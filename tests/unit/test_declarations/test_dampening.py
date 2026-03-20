"""Unit tests for declaration-aware score dampening (020)."""

from __future__ import annotations

from unittest.mock import MagicMock

import numpy as np

from eigenhelm.critic.aesthetic_critic import AestheticCritic


def _make_critic() -> AestheticCritic:
    return AestheticCritic(
        sigma_drift=1.0,
        sigma_virtue=1.0,
        reject_threshold=0.6,
        marginal_threshold=0.4,
    )


# Synthetic Python source that produces a non-trivial score
_SOURCE = """
from dataclasses import dataclass

@dataclass(frozen=True)
class Foo:
    name: str
    value: int

@dataclass(frozen=True)
class Bar:
    x: float
    y: float

@dataclass(frozen=True)
class Baz:
    a: str
    b: str

@dataclass(frozen=True)
class Qux:
    p: int
    q: int
"""


def test_dampened_score_less_than_undampened():
    """Declaration-dominant dampening should reduce the score."""
    critic = _make_critic()
    undampened = critic.evaluate(_SOURCE, "python")
    dampened = critic.evaluate(_SOURCE, "python", declaration_dominant=True)
    # Dampened should be <= undampened (may be equal if drift/alignment are 0)
    assert dampened.score.value <= undampened.score.value


def test_dampened_score_above_accept_threshold():
    """Dampened score must not go below the accept threshold (0.4)."""
    critic = _make_critic()
    result = critic.evaluate(_SOURCE, "python", declaration_dominant=True)
    assert result.score.value >= 0.4


def test_non_declaration_scores_identical():
    """When declaration_dominant=False, scores must be unchanged."""
    critic = _make_critic()
    baseline = critic.evaluate(_SOURCE, "python", declaration_dominant=False)
    default = critic.evaluate(_SOURCE, "python")
    assert baseline.score.value == default.score.value


def test_dampening_with_projection():
    """Dampening should reduce drift/alignment contributions with real projection."""
    critic = _make_critic()
    # Create a mock projection with high drift and alignment
    projection = MagicMock()
    projection.l_drift = 0.9
    projection.l_virtue = 0.8
    projection.quality_flag = "nominal"
    projection.coordinates = np.zeros(5)
    projection.x_norm = None
    projection.x_rec = None

    undampened = critic.evaluate(
        _SOURCE, "python", projection=projection, declaration_dominant=False
    )
    dampened = critic.evaluate(
        _SOURCE, "python", projection=projection, declaration_dominant=True
    )
    assert dampened.score.value < undampened.score.value
    assert dampened.score.value >= 0.4
