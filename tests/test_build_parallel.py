"""Unit tests for build_parallel — parallel dispatcher for build-agent."""
from __future__ import annotations

import asyncio
import textwrap
from typing import List
from unittest.mock import AsyncMock

import pytest

from build_parallel import (
    EvidenceRecord,
    ManifestTask,
    ParallelBuildConfig,
    TaskStatus,
    build_task_graph,
    group_independent_tasks,
    merge_evidence,
    parse_manifest,
    render_build_report_section,
    run_parallel_build,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _passing_evidence(task: ManifestTask) -> EvidenceRecord:
    return EvidenceRecord(
        task_id=task.id,
        manifest_index=task.manifest_index,
        file_path=task.file_path,
        agent_name=task.agent_name,
        gate_items=[{"name": "lint", "status": "PASS", "evidence": "ruff OK"}],
        verification={"lint": "PASS"},
        status="PASS",
    )


def _failing_evidence(task: ManifestTask, blocker: str = "Mandatory gate FAIL") -> EvidenceRecord:
    return EvidenceRecord(
        task_id=task.id,
        manifest_index=task.manifest_index,
        file_path=task.file_path,
        agent_name=task.agent_name,
        gate_items=[{"name": "lint", "status": "FAIL", "evidence": blocker}],
        verification={"lint": "FAIL"},
        status="FAIL",
        blocker=blocker,
    )


SAMPLE_DESIGN = textwrap.dedent("""\
    ## File Manifest

    | # | File | Action | Purpose | Dependencies |
    |---|------|--------|---------|--------------|
    | 1 | `config.yaml` | Create | Configuration | None |
    | 2 | `utils.py` | Create | Utilities | None |
    | 3 | `main.py` | Create | Entry point | 1, 2 |
    | 4 | `test_main.py` | Create | Tests | 3 |
""")

SAMPLE_DESIGN_WITH_AGENTS = textwrap.dedent("""\
    ## File Manifest

    | # | File | Action | Purpose | Dependencies | Agent |
    |---|------|--------|---------|--------------|-------|
    | 1 | `docker-compose.yml` | Create | Services | None | @{container-specialist} |
    | 2 | `models/orders.sql` | Create | dbt model | None | @{dbt-specialist} |
    | 3 | `dags/pipeline.py` | Create | Airflow DAG | 1, 2 | @{airflow-specialist} |
""")


# ---------------------------------------------------------------------------
# parse_manifest
# ---------------------------------------------------------------------------

class TestParseManifest:
    def test_parses_four_tasks(self):
        tasks = parse_manifest(SAMPLE_DESIGN)
        assert len(tasks) == 4

    def test_tasks_ordered_by_manifest_index(self):
        tasks = parse_manifest(SAMPLE_DESIGN)
        indices = [t.manifest_index for t in tasks]
        assert indices == sorted(indices)

    def test_deps_resolved_correctly(self):
        tasks = parse_manifest(SAMPLE_DESIGN)
        by_id = {t.id: t for t in tasks}
        assert by_id["3"].deps == {"1", "2"}
        assert by_id["4"].deps == {"3"}

    def test_no_agent_assigned_for_general_tasks(self):
        tasks = parse_manifest(SAMPLE_DESIGN)
        assert all(t.agent_name is None for t in tasks)

    def test_agents_parsed_from_manifest(self):
        tasks = parse_manifest(SAMPLE_DESIGN_WITH_AGENTS)
        by_id = {t.id: t for t in tasks}
        assert by_id["1"].agent_name == "container-specialist"
        assert by_id["2"].agent_name == "dbt-specialist"
        assert by_id["3"].agent_name == "airflow-specialist"

    def test_independent_tasks_have_no_deps(self):
        tasks = parse_manifest(SAMPLE_DESIGN)
        by_id = {t.id: t for t in tasks}
        assert by_id["1"].deps == set()
        assert by_id["2"].deps == set()

    def test_empty_manifest_returns_empty_list(self):
        assert parse_manifest("No manifest table here.") == []

    def test_retries_default_applied(self):
        tasks = parse_manifest(SAMPLE_DESIGN, default_retries=5)
        assert all(t.retries_left == 5 for t in tasks)


# ---------------------------------------------------------------------------
# build_task_graph / group_independent_tasks
# ---------------------------------------------------------------------------

class TestTaskGraph:
    def setup_method(self):
        self.tasks = parse_manifest(SAMPLE_DESIGN)
        self.graph = build_task_graph(self.tasks)

    def test_all_tasks_in_graph(self):
        assert set(self.graph.tasks.keys()) == {"1", "2", "3", "4"}

    def test_in_degree_for_independent_tasks_is_zero(self):
        assert self.graph.in_degree["1"] == 0
        assert self.graph.in_degree["2"] == 0

    def test_in_degree_for_dependent_tasks(self):
        assert self.graph.in_degree["3"] == 2
        assert self.graph.in_degree["4"] == 1

    def test_group_produces_correct_waves(self):
        waves = group_independent_tasks(self.graph)
        assert len(waves) == 3
        wave_ids = [sorted(t.id for t in w) for w in waves]
        assert wave_ids[0] == ["1", "2"]
        assert wave_ids[1] == ["3"]
        assert wave_ids[2] == ["4"]

    def test_cycle_raises_value_error(self):
        from build_parallel import ManifestTask, build_task_graph, group_independent_tasks
        a = ManifestTask("a", 1, "a.py", "Create", "A", None, deps={"b"})
        b = ManifestTask("b", 2, "b.py", "Create", "B", None, deps={"a"})
        g = build_task_graph([a, b])
        with pytest.raises(ValueError, match="Cycle detected"):
            group_independent_tasks(g)


# ---------------------------------------------------------------------------
# run_parallel_build — success path
# ---------------------------------------------------------------------------

class TestRunParallelBuild:
    def test_all_tasks_completed(self):
        tasks = parse_manifest(SAMPLE_DESIGN)
        graph = build_task_graph(tasks)
        config = ParallelBuildConfig(concurrency=6)

        async def mock_subagent(task):
            await asyncio.sleep(0)
            return _passing_evidence(task)

        results = run_parallel_build(graph, mock_subagent, config)
        assert len(results) == 4
        assert all(r.status == "PASS" for r in results)

    def test_results_use_manifest_index_order_after_merge(self):
        tasks = parse_manifest(SAMPLE_DESIGN)
        graph = build_task_graph(tasks)
        config = ParallelBuildConfig(concurrency=6)

        async def mock_subagent(task):
            await asyncio.sleep(0)
            return _passing_evidence(task)

        raw = run_parallel_build(graph, mock_subagent, config)
        merged = merge_evidence(raw)
        indices = [r.manifest_index for r in merged]
        assert indices == sorted(indices)

    def test_concurrency_one_runs_serial(self):
        call_order: List[str] = []
        tasks = parse_manifest(SAMPLE_DESIGN)
        graph = build_task_graph(tasks)
        config = ParallelBuildConfig(concurrency=1, enabled=True)

        async def mock_subagent(task):
            call_order.append(task.id)
            return _passing_evidence(task)

        run_parallel_build(graph, mock_subagent, config)
        assert call_order == sorted(call_order, key=lambda x: int(x))

    def test_disabled_falls_back_to_serial(self):
        tasks = parse_manifest(SAMPLE_DESIGN)
        graph = build_task_graph(tasks)
        config = ParallelBuildConfig(enabled=False)

        async def mock_subagent(task):
            return _passing_evidence(task)

        results = run_parallel_build(graph, mock_subagent, config)
        assert len(results) == 4


# ---------------------------------------------------------------------------
# run_parallel_build — failure paths
# ---------------------------------------------------------------------------

class TestRunParallelBuildFailures:
    def test_critical_failure_raises_runtime_error(self):
        tasks = parse_manifest(SAMPLE_DESIGN)
        graph = build_task_graph(tasks)
        config = ParallelBuildConfig(
            concurrency=6,
            stop_on_critical_failure=True,
            retry_limit=1,
        )

        async def failing_subagent(task):
            return _failing_evidence(task, blocker="Mandatory gate FAIL")

        with pytest.raises(RuntimeError, match="Critical failure"):
            run_parallel_build(graph, failing_subagent, config)

    def test_no_stop_on_non_critical_failure(self):
        tasks = parse_manifest(SAMPLE_DESIGN)
        graph = build_task_graph(tasks)
        config = ParallelBuildConfig(
            concurrency=6,
            stop_on_critical_failure=False,
            retry_limit=1,
        )

        async def failing_subagent(task):
            return _failing_evidence(task, blocker="minor issue")

        results = run_parallel_build(graph, failing_subagent, config)
        assert len(results) == 4

    def test_retry_on_transient_failure(self):
        call_counts: dict = {}
        tasks = parse_manifest(SAMPLE_DESIGN)
        graph = build_task_graph(tasks)
        config = ParallelBuildConfig(
            concurrency=6,
            retry_limit=3,
            stop_on_critical_failure=False,
        )

        async def flaky_subagent(task):
            call_counts[task.id] = call_counts.get(task.id, 0) + 1
            if call_counts[task.id] < 2:
                return EvidenceRecord(
                    task_id=task.id,
                    manifest_index=task.manifest_index,
                    file_path=task.file_path,
                    agent_name=task.agent_name,
                    gate_items=[],
                    verification={},
                    status="FAIL",
                )
            return _passing_evidence(task)

        results = run_parallel_build(graph, flaky_subagent, config)
        assert all(r.status == "PASS" for r in results)
        assert all(v >= 2 for v in call_counts.values())

    def test_timeout_recorded_as_fail(self):
        tasks = parse_manifest(SAMPLE_DESIGN)
        graph = build_task_graph(tasks)
        config = ParallelBuildConfig(
            concurrency=6,
            task_timeout_sec=1,
            retry_limit=1,
            stop_on_critical_failure=False,
        )

        async def slow_subagent(task):
            await asyncio.sleep(10)
            return _passing_evidence(task)

        results = run_parallel_build(graph, slow_subagent, config)
        assert all(r.status == "FAIL" for r in results)
        assert all("Timeout" in (r.blocker or "") for r in results)


# ---------------------------------------------------------------------------
# merge_evidence + render_build_report_section
# ---------------------------------------------------------------------------

class TestMergeAndRender:
    def _make_records(self, indices: list) -> List[EvidenceRecord]:
        records = []
        for i in indices:
            task = ManifestTask(str(i), i, f"file_{i}.py", "Create", "X", None)
            records.append(_passing_evidence(task))
        return records

    def test_merge_sorts_by_manifest_index(self):
        records = self._make_records([4, 1, 3, 2])
        merged = merge_evidence(records)
        assert [r.manifest_index for r in merged] == [1, 2, 3, 4]

    def test_render_includes_all_files(self):
        records = self._make_records([1, 2, 3])
        report = render_build_report_section(records)
        for i in [1, 2, 3]:
            assert f"file_{i}.py" in report

    def test_render_marks_direct_agent_when_none(self):
        records = self._make_records([1])
        report = render_build_report_section(records)
        assert "(direct)" in report

    def test_render_marks_specialist_agent_when_set(self):
        task = ManifestTask("1", 1, "docker-compose.yml", "Create", "Services", "container-specialist")
        record = _passing_evidence(task)
        report = render_build_report_section([record])
        assert "container-specialist" in report

    def test_render_shows_blocker_in_notes(self):
        task = ManifestTask("1", 1, "main.py", "Create", "Entry", None)
        record = _failing_evidence(task, blocker="Docker Hub image not found")
        report = render_build_report_section([record])
        assert "Docker Hub image not found" in report
