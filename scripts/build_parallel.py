"""build_parallel — parallel dispatcher for the build-agent.

Extracts a task graph from a DESIGN file manifest, groups independent
tasks, and dispatches runSubagent calls concurrently up to a configurable
concurrency limit.

Usage (programmatic, by build-agent):

    from build_parallel import (
        parse_manifest,
        build_task_graph,
        run_parallel_build,
        merge_evidence,
    )

    tasks = parse_manifest(design_content)
    graph = build_task_graph(tasks)
    evidence_store = run_parallel_build(graph, subagent_fn, config)
    report_rows = merge_evidence(evidence_store)
"""
from __future__ import annotations

import asyncio
import re
import time
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Awaitable, Callable, Dict, List, Optional, Set


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class ManifestTask:
    id: str
    manifest_index: int
    file_path: str
    action: str
    purpose: str
    agent_name: Optional[str]
    deps: Set[str] = field(default_factory=set)
    status: TaskStatus = TaskStatus.PENDING
    retries_left: int = 3


@dataclass
class EvidenceRecord:
    task_id: str
    manifest_index: int
    file_path: str
    agent_name: Optional[str]
    gate_items: List[Dict[str, str]]
    verification: Dict[str, str]
    status: str
    blocker: Optional[str] = None
    timestamp: float = field(default_factory=time.time)


@dataclass
class TaskGraph:
    tasks: Dict[str, ManifestTask]
    in_degree: Dict[str, int]
    dependents: Dict[str, List[str]]


@dataclass
class ParallelBuildConfig:
    concurrency: int = 6
    task_timeout_sec: int = 600
    retry_limit: int = 3
    stop_on_critical_failure: bool = True
    enabled: bool = True


# ---------------------------------------------------------------------------
# Manifest parser
# ---------------------------------------------------------------------------

_MANIFEST_ROW_RE = re.compile(
    r"\|\s*(?P<idx>\d+)\s*\|"
    r"\s*`?(?P<path>[^|`]+?)`?\s*\|"
    r"\s*(?P<action>[^|]+?)\s*\|"
    r"\s*(?P<purpose>[^|]+?)\s*\|"
    r"\s*(?P<deps>[^|]*?)\s*\|"
    r"(?:\s*@?(?P<agent>[A-Za-z0-9._-]+?)\s*\|)?",
    re.IGNORECASE,
)

_AGENT_INLINE_RE = re.compile(r"@\{?([A-Za-z0-9._-]+)\}?")


def parse_manifest(design_content: str, default_retries: int = 3) -> List[ManifestTask]:
    """Parse the file manifest table from a DESIGN document.

    Rows must follow the manifest table format produced by design-agent:
        | # | File | Action | Purpose | Dependencies | Agent (optional) |

    Returns tasks ordered by manifest_index.
    """
    tasks: List[ManifestTask] = []
    raw_dep_map: Dict[str, str] = {}

    for match in _MANIFEST_ROW_RE.finditer(design_content):
        idx = int(match.group("idx"))
        path = match.group("path").strip()
        action = match.group("action").strip()
        purpose = match.group("purpose").strip()
        raw_deps = (match.group("deps") or "").strip()
        agent_raw = match.group("agent") or ""

        agent_name: Optional[str] = None
        inline = _AGENT_INLINE_RE.search(design_content[match.start():match.end() + 200])
        if inline:
            agent_name = inline.group(1)
        elif agent_raw and agent_raw.lower() not in ("none", "general", "(general)", ""):
            agent_name = agent_raw.strip()

        task = ManifestTask(
            id=str(idx),
            manifest_index=idx,
            file_path=path,
            action=action,
            purpose=purpose,
            agent_name=agent_name,
            retries_left=default_retries,
        )
        tasks.append(task)
        raw_dep_map[str(idx)] = raw_deps

    _resolve_deps(tasks, raw_dep_map)
    return sorted(tasks, key=lambda t: t.manifest_index)


def _resolve_deps(tasks: List[ManifestTask], raw_dep_map: Dict[str, str]) -> None:
    id_set = {t.id for t in tasks}
    for task in tasks:
        raw = raw_dep_map.get(task.id, "")
        for token in re.split(r"[,\s]+", raw):
            token = token.strip()
            if token and token in id_set and token != task.id:
                task.deps.add(token)


# ---------------------------------------------------------------------------
# Task graph builder
# ---------------------------------------------------------------------------

def build_task_graph(tasks: List[ManifestTask]) -> TaskGraph:
    """Compute in-degree counts and dependents index from the task list."""
    in_degree: Dict[str, int] = {t.id: 0 for t in tasks}
    dependents: Dict[str, List[str]] = defaultdict(list)

    for task in tasks:
        for dep_id in task.deps:
            in_degree[task.id] = in_degree.get(task.id, 0) + 1
            dependents[dep_id].append(task.id)

    return TaskGraph(
        tasks={t.id: t for t in tasks},
        in_degree=in_degree,
        dependents=dict(dependents),
    )


def group_independent_tasks(graph: TaskGraph) -> List[List[ManifestTask]]:
    """Return tasks grouped into dependency-ordered batches (waves).

    Each wave contains all tasks whose dependencies are satisfied by the
    preceding waves, enabling intra-wave parallel execution.
    """
    remaining_in_degree = dict(graph.in_degree)
    waves: List[List[ManifestTask]] = []
    visited: Set[str] = set()

    while len(visited) < len(graph.tasks):
        wave = [
            graph.tasks[tid]
            for tid, deg in remaining_in_degree.items()
            if deg == 0 and tid not in visited
        ]
        if not wave:
            not_done = set(graph.tasks) - visited
            raise ValueError(
                f"Cycle detected in task graph. Unresolved tasks: {not_done}"
            )
        wave_sorted = sorted(wave, key=lambda t: t.manifest_index)
        waves.append(wave_sorted)
        for task in wave_sorted:
            visited.add(task.id)
            for dep_id in graph.dependents.get(task.id, []):
                remaining_in_degree[dep_id] -= 1

    return waves


# ---------------------------------------------------------------------------
# Parallel dispatcher
# ---------------------------------------------------------------------------

SubagentFn = Callable[[ManifestTask], Awaitable[EvidenceRecord]]


async def _run_task_with_retry(
    task: ManifestTask,
    subagent_fn: SubagentFn,
    config: ParallelBuildConfig,
) -> EvidenceRecord:
    backoff = 5
    last_record: Optional[EvidenceRecord] = None

    for attempt in range(config.retry_limit):
        try:
            record = await asyncio.wait_for(
                subagent_fn(task),
                timeout=config.task_timeout_sec,
            )
            if record.status == "PASS":
                task.status = TaskStatus.DONE
                return record
            last_record = record
            if record.blocker:
                task.status = TaskStatus.BLOCKED
                return record
        except asyncio.TimeoutError:
            last_record = EvidenceRecord(
                task_id=task.id,
                manifest_index=task.manifest_index,
                file_path=task.file_path,
                agent_name=task.agent_name,
                gate_items=[],
                verification={},
                status="FAIL",
                blocker=f"Timeout after {config.task_timeout_sec}s (attempt {attempt + 1})",
            )
        except Exception as exc:
            last_record = EvidenceRecord(
                task_id=task.id,
                manifest_index=task.manifest_index,
                file_path=task.file_path,
                agent_name=task.agent_name,
                gate_items=[],
                verification={},
                status="FAIL",
                blocker=str(exc),
            )

        if attempt < config.retry_limit - 1:
            await asyncio.sleep(backoff)
            backoff *= 2

    task.status = TaskStatus.FAILED
    assert last_record is not None
    return last_record


async def _dispatch_wave(
    wave: List[ManifestTask],
    subagent_fn: SubagentFn,
    config: ParallelBuildConfig,
    semaphore: asyncio.Semaphore,
) -> List[EvidenceRecord]:
    async def bounded(task: ManifestTask) -> EvidenceRecord:
        async with semaphore:
            return await _run_task_with_retry(task, subagent_fn, config)

    return list(await asyncio.gather(*[bounded(t) for t in wave]))


async def _run_parallel_build_async(
    graph: TaskGraph,
    subagent_fn: SubagentFn,
    config: ParallelBuildConfig,
) -> List[EvidenceRecord]:
    if not config.enabled or config.concurrency <= 1:
        return await _serial_build(graph, subagent_fn, config)

    semaphore = asyncio.Semaphore(config.concurrency)
    waves = group_independent_tasks(graph)
    all_evidence: List[EvidenceRecord] = []

    for wave in waves:
        wave_results = await _dispatch_wave(wave, subagent_fn, config, semaphore)
        all_evidence.extend(wave_results)

        if config.stop_on_critical_failure:
            critical = [r for r in wave_results if r.blocker and r.status == "FAIL"]
            if critical:
                blocker_summary = "; ".join(r.blocker or "" for r in critical)
                raise RuntimeError(
                    f"Critical failure(s) halted build: {blocker_summary}"
                )

    return all_evidence


async def _serial_build(
    graph: TaskGraph,
    subagent_fn: SubagentFn,
    config: ParallelBuildConfig,
) -> List[EvidenceRecord]:
    waves = group_independent_tasks(graph)
    results: List[EvidenceRecord] = []
    for wave in waves:
        for task in wave:
            results.append(await _run_task_with_retry(task, subagent_fn, config))
    return results


def run_parallel_build(
    graph: TaskGraph,
    subagent_fn: SubagentFn,
    config: Optional[ParallelBuildConfig] = None,
) -> List[EvidenceRecord]:
    """Synchronous entry point — runs the async dispatcher in an event loop.

    Args:
        graph: TaskGraph produced by build_task_graph().
        subagent_fn: Async callable that receives a ManifestTask and returns
                     an EvidenceRecord. This wraps agent.runSubagent() in the
                     build-agent context.
        config: Optional ParallelBuildConfig; defaults to ParallelBuildConfig().

    Returns:
        Unsorted list of EvidenceRecord (use merge_evidence to sort).

    Raises:
        RuntimeError: When stop_on_critical_failure=True and a critical failure
                      is detected in any wave.
        ValueError: When a dependency cycle is detected in the task graph.
    """
    cfg = config or ParallelBuildConfig()
    return asyncio.run(_run_parallel_build_async(graph, subagent_fn, cfg))


# ---------------------------------------------------------------------------
# Evidence merger
# ---------------------------------------------------------------------------

def merge_evidence(records: List[EvidenceRecord]) -> List[EvidenceRecord]:
    """Sort evidence records by manifest_index for deterministic BUILD_REPORT."""
    return sorted(records, key=lambda r: (r.manifest_index, r.task_id))


def render_build_report_section(records: List[EvidenceRecord]) -> str:
    """Render the Tasks-with-Attribution and Specialist-Gate-Evidence sections."""
    sorted_records = merge_evidence(records)
    lines: List[str] = []

    lines.append("## Tasks with Attribution\n")
    lines.append("| Task | Agent | Status | Notes |")
    lines.append("|------|-------|--------|-------|")
    for r in sorted_records:
        agent = f"@{{{r.agent_name}}}" if r.agent_name else "(direct)"
        icon = "✅" if r.status == "PASS" else ("🔴" if r.blocker else "⚠️")
        notes = r.blocker or "OK"
        lines.append(f"| {r.file_path} | {agent} | {icon} | {notes} |")

    lines.append("\n## Specialist Gate Evidence\n")
    lines.append("| File | Agent | Gate | Evidence | Status |")
    lines.append("|------|-------|------|----------|--------|")
    for r in sorted_records:
        if not r.gate_items:
            continue
        agent = r.agent_name or "direct"
        for item in r.gate_items:
            icon = "✅" if item.get("status") == "PASS" else "❌"
            lines.append(
                f"| {r.file_path} | {agent} "
                f"| {item.get('name', '')} "
                f"| {item.get('evidence', '')} "
                f"| {icon} |"
            )

    return "\n".join(lines) + "\n"
