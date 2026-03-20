"""Data models for test code region detection and scoring."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RegionType(Enum):
    """Classification of a code region."""

    PRODUCTION = "production"
    TEST = "test"


@dataclass(frozen=True)
class TestBoundary:
    """A detected test code boundary in the AST.

    Internal to the regions module — not exposed in output.
    """

    start_line: int  # 1-indexed
    end_line: int  # 1-indexed
    language: str
    pattern: str  # e.g., "cfg_test_module", "test_class", "test_function"

    def __post_init__(self) -> None:
        if self.start_line > self.end_line:
            raise ValueError(
                f"start_line ({self.start_line}) must be <= end_line ({self.end_line})"
            )


@dataclass(frozen=True)
class RegionSpan:
    """A contiguous line range within a file, labeled by type."""

    label: RegionType
    start_line: int  # 1-indexed
    end_line: int  # 1-indexed

    def __post_init__(self) -> None:
        if self.start_line > self.end_line:
            raise ValueError(
                f"start_line ({self.start_line}) must be <= end_line ({self.end_line})"
            )


@dataclass(frozen=True)
class RegionSummary:
    """Aggregated score for all spans sharing a label.

    This is what appears in output. Consumers select by label, not array position.
    """

    label: RegionType
    spans: tuple[RegionSpan, ...]
    total_lines: int
    score: float  # [0.0, 1.0]
    decision: str  # "accept", "warn", "reject"
    percentile: float | None  # 0-100, or None if unavailable
