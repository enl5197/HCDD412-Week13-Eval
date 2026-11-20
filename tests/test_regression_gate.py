
"""Tests for the regression gate."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "evals"))

import run_evals  # noqa: E402


def test_gate_flags_case_that_used_to_pass():
    baseline = {"results": [{"id": "a", "passed": True}], "pass_rate": 1.0}
    current = {"results": [{"id": "a", "passed": False}], "pass_rate": 0.0}

    problems = run_evals.regression_gate(baseline, current)

    assert problems
    assert "a" in problems[0]


def test_gate_allows_identical_runs():
    report = {"results": [{"id": "a", "passed": True}], "pass_rate": 1.0}

    assert run_evals.regression_gate(report, report) == []


def test_gate_allows_new_case():
    baseline = {
        "results": [{"id": "a", "passed": True}],
        "pass_rate": 1.0,
    }
    current = {
        "results": [
            {"id": "a", "passed": True},
            {"id": "b", "passed": True},
        ],
        "pass_rate": 1.0,
    }

    assert run_evals.regression_gate(baseline, current) == []


def test_gate_allows_previously_failing_case_to_pass():
    baseline = {
        "results": [{"id": "a", "passed": False}],
        "pass_rate": 0.0,
    }
    current = {
        "results": [{"id": "a", "passed": True}],
        "pass_rate": 1.0,
    }

    assert run_evals.regression_gate(baseline, current) == []


def test_gate_flags_missing_previously_passing_case():
    baseline = {
        "results": [{"id": "a", "passed": True}],
        "pass_rate": 1.0,
    }
    current = {"results": [], "pass_rate": 0.0}

    problems = run_evals.regression_gate(baseline, current)

    assert problems
    assert "missing from the current run" in problems[0]
