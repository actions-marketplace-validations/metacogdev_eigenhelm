"""Integration tests for region output formatting (019-test-code-split T014)."""

from __future__ import annotations

from pathlib import Path

import pytest

from eigenhelm.cli.evaluate import format_result_human

_FIXTURES = Path(__file__).parent.parent / "fixtures" / "regions"


@pytest.fixture
def helm():
    from eigenhelm.helm import DynamicHelm
    from eigenhelm.trained_models import default_model_path
    from eigenhelm.eigenspace import load_model

    model = load_model(str(default_model_path()))
    return DynamicHelm(eigenspace=model)


@pytest.mark.requires_model
def test_human_output_shows_regions_for_python_with_tests(helm):
    """Files with test code show a regions: block in human output."""
    from eigenhelm.helm.models import EvaluationRequest
    from eigenhelm.cli.evaluate import _attach_regions

    source = (_FIXTURES / "python_with_tests.py").read_text()
    resp = helm.evaluate(EvaluationRequest(source=source, language="python"))
    resp = _attach_regions(resp, source, "python", helm)

    output = format_result_human("test.py", resp, classify=True)
    assert "regions:" in output
    assert "production" in output
    assert "test" in output


@pytest.mark.requires_model
def test_human_output_no_regions_for_no_test_file(helm):
    """Files without test code produce output with no regions: block."""
    from eigenhelm.helm.models import EvaluationRequest
    from eigenhelm.cli.evaluate import _attach_regions

    source = (_FIXTURES / "python_no_tests.py").read_text()
    resp = helm.evaluate(EvaluationRequest(source=source, language="python"))
    resp = _attach_regions(resp, source, "python", helm)

    output = format_result_human("test.py", resp, classify=True)
    assert "regions:" not in output
