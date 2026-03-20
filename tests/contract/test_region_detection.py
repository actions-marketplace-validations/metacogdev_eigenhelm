"""Contract tests for test boundary detection (019-test-code-split).

Validates invariants from contracts/region-detection.md:
- Empty result for no-test files
- Correct boundaries for Rust/Python fixtures
- No overlapping boundaries
- Conservative detection (no false positives)
"""

from __future__ import annotations

from pathlib import Path


from eigenhelm.regions import detect_test_boundaries
from eigenhelm.regions.models import TestBoundary

_FIXTURES = Path(__file__).parent.parent / "fixtures" / "regions"


# ---------------------------------------------------------------------------
# Invariant 1: Empty result for no-test files
# ---------------------------------------------------------------------------


def test_no_tests_python():
    source = (_FIXTURES / "python_no_tests.py").read_text()
    result = detect_test_boundaries(source, "python")
    assert result == ()


def test_unsupported_language_returns_empty():
    result = detect_test_boundaries("fn main() {}", "go")
    assert result == ()


def test_empty_source_returns_empty():
    result = detect_test_boundaries("", "python")
    assert result == ()


# ---------------------------------------------------------------------------
# Invariant 2: start_line <= end_line
# ---------------------------------------------------------------------------


def test_boundary_line_ordering_rust():
    source = (_FIXTURES / "rust_with_tests.rs").read_text()
    boundaries = detect_test_boundaries(source, "rust")
    for b in boundaries:
        assert b.start_line <= b.end_line, f"Invalid boundary: {b}"


def test_boundary_line_ordering_python():
    source = (_FIXTURES / "python_with_tests.py").read_text()
    boundaries = detect_test_boundaries(source, "python")
    for b in boundaries:
        assert b.start_line <= b.end_line, f"Invalid boundary: {b}"


# ---------------------------------------------------------------------------
# Invariant 3: No overlapping boundaries
# ---------------------------------------------------------------------------


def test_no_overlapping_boundaries_rust():
    source = (_FIXTURES / "rust_with_tests.rs").read_text()
    boundaries = detect_test_boundaries(source, "rust")
    _assert_no_overlaps(boundaries)


def test_no_overlapping_boundaries_python():
    source = (_FIXTURES / "python_with_tests.py").read_text()
    boundaries = detect_test_boundaries(source, "python")
    _assert_no_overlaps(boundaries)


# ---------------------------------------------------------------------------
# Correct detection: Rust #[cfg(test)]
# ---------------------------------------------------------------------------


def test_rust_detects_cfg_test_module():
    source = (_FIXTURES / "rust_with_tests.rs").read_text()
    boundaries = detect_test_boundaries(source, "rust")
    assert len(boundaries) == 1
    assert boundaries[0].pattern == "cfg_test_module"
    assert boundaries[0].language == "rust"
    # The #[cfg(test)] mod tests block starts around line 77 and goes to EOF
    total_lines = len(source.splitlines())
    assert boundaries[0].end_line == total_lines


# ---------------------------------------------------------------------------
# Correct detection: Python test classes and functions
# ---------------------------------------------------------------------------


def test_python_detects_test_class():
    source = (_FIXTURES / "python_with_tests.py").read_text()
    boundaries = detect_test_boundaries(source, "python")
    class_boundaries = [b for b in boundaries if b.pattern == "test_class"]
    assert len(class_boundaries) >= 1
    assert all(b.language == "python" for b in class_boundaries)


def test_python_detects_test_functions():
    source = (_FIXTURES / "python_with_tests.py").read_text()
    boundaries = detect_test_boundaries(source, "python")
    func_boundaries = [b for b in boundaries if b.pattern == "test_function"]
    assert len(func_boundaries) >= 1


def test_python_pure_test_file():
    source = (_FIXTURES / "python_pure_tests.py").read_text()
    boundaries = detect_test_boundaries(source, "python")
    assert len(boundaries) >= 2  # At least 2 test classes + standalone function


# ---------------------------------------------------------------------------
# Invariant 6: Conservative detection — no false positives
# ---------------------------------------------------------------------------


def test_python_no_false_positives_on_production():
    """Production code in python_no_tests.py must not be classified as test."""
    source = (_FIXTURES / "python_no_tests.py").read_text()
    boundaries = detect_test_boundaries(source, "python")
    assert boundaries == ()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _assert_no_overlaps(boundaries: tuple[TestBoundary, ...]) -> None:
    """Assert that boundaries are sorted and non-overlapping."""
    for i in range(len(boundaries) - 1):
        assert boundaries[i].end_line < boundaries[i + 1].start_line, (
            f"Overlapping boundaries: {boundaries[i]} and {boundaries[i + 1]}"
        )
