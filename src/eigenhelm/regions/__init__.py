"""Test code region detection and scoring.

Detects test code boundaries within source files using language-specific
heuristics, derives production/test region spans, and scores each region
independently.

Public API:
    detect_test_boundaries() — find test code line ranges
    derive_spans() — convert boundaries to labeled region spans
"""

from __future__ import annotations

from eigenhelm.regions.models import (
    RegionSpan,
    RegionSummary,
    RegionType,
    TestBoundary,
)

__all__ = [
    "RegionSpan",
    "RegionSummary",
    "RegionType",
    "TestBoundary",
    "derive_spans",
    "detect_test_boundaries",
]


def detect_test_boundaries(source: str, language: str) -> tuple[TestBoundary, ...]:
    """Detect test code boundaries in source using language-specific heuristics.

    Parses the source internally. Returns an empty tuple for unsupported
    languages or when no test code is detected.

    Args:
        source: Raw source code string.
        language: Language identifier (e.g., "python", "rust").

    Returns:
        Tuple of TestBoundary entries, sorted by start_line.
    """
    if not source.strip():
        return ()

    if language == "rust":
        from eigenhelm.regions.rust import detect

        return detect(source)
    if language == "python":
        from eigenhelm.regions.python import detect

        return detect(source)

    return ()


def derive_spans(
    boundaries: tuple[TestBoundary, ...],
    total_lines: int,
) -> tuple[RegionSpan, ...]:
    """Convert test boundaries to a complete set of labeled region spans.

    All lines in the file are covered: lines within boundaries are test spans,
    lines outside are production spans. Production spans may be empty if the
    entire file is test code.

    Args:
        boundaries: Sorted, non-overlapping TestBoundary entries.
        total_lines: Total line count in the source file.

    Returns:
        Tuple of RegionSpan entries, sorted by start_line.
    """
    if not boundaries:
        return ()

    spans: list[RegionSpan] = []
    current_line = 1

    for b in boundaries:
        # Production span before this test boundary
        if b.start_line > current_line:
            spans.append(
                RegionSpan(
                    label=RegionType.PRODUCTION,
                    start_line=current_line,
                    end_line=b.start_line - 1,
                )
            )
        # Test span
        spans.append(
            RegionSpan(
                label=RegionType.TEST,
                start_line=b.start_line,
                end_line=b.end_line,
            )
        )
        current_line = b.end_line + 1

    # Trailing production span
    if current_line <= total_lines:
        spans.append(
            RegionSpan(
                label=RegionType.PRODUCTION,
                start_line=current_line,
                end_line=total_lines,
            )
        )

    return tuple(spans)
