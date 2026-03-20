"""Unit tests for per-region scoring (019-test-code-split T013)."""

from __future__ import annotations

from pathlib import Path

import pytest

from eigenhelm.regions.models import RegionType

_FIXTURES = Path(__file__).parent.parent / "fixtures" / "regions"


@pytest.fixture
def helm():
    """Create a DynamicHelm with the default bundled model."""
    from eigenhelm.helm import DynamicHelm
    from eigenhelm.trained_models import default_model_path
    from eigenhelm.eigenspace import load_model

    model = load_model(str(default_model_path()))
    return DynamicHelm(eigenspace=model)


@pytest.mark.requires_model
def test_score_regions_returns_summaries(helm):
    """score_regions produces RegionSummary entries for each label."""
    source = (_FIXTURES / "python_with_tests.py").read_text()
    from eigenhelm.regions import detect_test_boundaries, derive_spans

    boundaries = detect_test_boundaries(source, "python")
    spans = derive_spans(boundaries, len(source.splitlines()))

    regions = helm.score_regions(source, "python", spans)
    assert len(regions) >= 2

    labels = {r.label for r in regions}
    assert RegionType.PRODUCTION in labels
    assert RegionType.TEST in labels


@pytest.mark.requires_model
def test_region_scores_are_valid(helm):
    """Each region score is in [0, 1] with a valid decision."""
    source = (_FIXTURES / "python_with_tests.py").read_text()
    from eigenhelm.regions import detect_test_boundaries, derive_spans

    boundaries = detect_test_boundaries(source, "python")
    spans = derive_spans(boundaries, len(source.splitlines()))
    regions = helm.score_regions(source, "python", spans)

    for r in regions:
        assert 0.0 <= r.score <= 1.0
        assert r.decision in ("accept", "warn", "reject")
        assert r.total_lines > 0


@pytest.mark.requires_model
def test_no_spans_returns_empty(helm):
    """Empty spans produce empty regions."""
    regions = helm.score_regions("x = 1\n", "python", ())
    assert regions == ()
