"""Unit tests for the validate skill's deterministic contract."""
from __future__ import annotations

import sys
from pathlib import Path


_VALIDATE_ROOT = Path(__file__).resolve().parent.parent / ".github" / "skills" / "validate"
if str(_VALIDATE_ROOT) not in sys.path:
    sys.path.insert(0, str(_VALIDATE_ROOT))


def test_council_report_computes_score_and_artifact_plan_in_code():
    from scripts.crews.council_crew import _build_deterministic_report
    from scripts.schemas import (
        CodeReport,
        DeliveryDelta,
        Finding,
        Severity,
        SpecReport,
        ValidateContext,
    )

    ctx = ValidateContext(
        feature_name="VALIDATE_WORKFLOW",
        define_content="define",
        design_content="design",
        build_report_content="build",
        code_tree=[".github/skills/validate/scripts/main.py"],
    )
    spec = SpecReport(
        feature="VALIDATE_WORKFLOW",
        alignment_score=90,
        architecture_score=80,
        requirement_coverage=90,
        findings=[],
        status="PASSED",
    )
    code = CodeReport(
        feature="VALIDATE_WORKFLOW",
        quality_score=70,
        devops_score=60,
        test_coverage=None,
        lint_issues=0,
        type_errors=0,
        findings=[
            Finding(
                title="Missing test",
                description="Add coverage for artifact rendering.",
                severity=Severity.MEDIUM,
                category="Coverage",
            )
        ],
        status="WARNING",
    )
    delivery = DeliveryDelta(
        feature="VALIDATE_WORKFLOW",
        delta_score=75,
        status="WARNING",
    )

    report = _build_deterministic_report(ctx, spec, code, delivery, summary="json guidance")

    assert report.score == 77.0
    assert report.status == "WARNING"
    assert report.runbook_eligible is False
    assert report.roadmap_eligible is True
    assert report.artifact_plan["recommended_artifact"] == "ROADMAP"
    assert report.artifact_plan["create_roadmap"] is True


def test_artifact_rendering_uses_templates_without_llm_markdown():
    from scripts.main import _render_validation_report
    from scripts.schemas import ValidationReport

    report = ValidationReport(
        feature="VALIDATE_WORKFLOW",
        score=92,
        status="PASSED",
        dimensions={
            "Spec Alignment": 95,
            "Code Quality": 90,
            "Architecture Fidelity": 92,
            "Security & DevOps": 88,
            "Production Readiness": 94,
        },
        critical_issues=[],
        findings=[],
        runbook_eligible=True,
        roadmap_eligible=False,
        summary="Ready based on JSON guidance.",
        artifact_plan={"recommended_artifact": "RUNBOOK"},
    )

    rendered = _render_validation_report("VALIDATE_WORKFLOW", report)

    assert rendered.startswith("# VALIDATION REPORT: VALIDATE_WORKFLOW")
    assert "Ready based on JSON guidance." in rendered
    assert "{XX}" not in rendered
    assert "{Brief summary" not in rendered
