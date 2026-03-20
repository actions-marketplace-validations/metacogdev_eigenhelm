"""Python test boundary detection via tree-sitter.

Detects class Test* and top-level def test_* patterns.
"""

from __future__ import annotations

from eigenhelm.regions.models import TestBoundary


def detect(source: str) -> tuple[TestBoundary, ...]:
    """Detect Python test code boundaries.

    Finds:
    - Top-level class definitions whose name starts with "Test"
    - Top-level function definitions whose name starts with "test_"

    Does NOT classify `if __name__ == "__main__"` as test code.

    Returns:
        Sorted, non-overlapping TestBoundary entries.
    """
    from eigenhelm.parsers.tree_sitter import parse_source

    root = parse_source(source, "python")
    if root is None:
        return ()

    boundaries: list[TestBoundary] = []

    for node in root.children:
        if node.type == "class_definition":
            name = _extract_name(node)
            if name.startswith("Test"):
                boundaries.append(
                    TestBoundary(
                        start_line=node.start_point[0] + 1,
                        end_line=node.end_point[0] + 1,
                        language="python",
                        pattern="test_class",
                    )
                )
        elif node.type == "function_definition":
            name = _extract_name(node)
            if name.startswith("test_"):
                boundaries.append(
                    TestBoundary(
                        start_line=node.start_point[0] + 1,
                        end_line=node.end_point[0] + 1,
                        language="python",
                        pattern="test_function",
                    )
                )
        elif node.type == "decorated_definition":
            # Handle @decorator\ndef test_foo / class TestBar
            inner = _get_decorated_inner(node)
            if inner is not None:
                name = _extract_name(inner)
                if inner.type == "class_definition" and name.startswith("Test"):
                    boundaries.append(
                        TestBoundary(
                            start_line=node.start_point[0] + 1,
                            end_line=node.end_point[0] + 1,
                            language="python",
                            pattern="test_class",
                        )
                    )
                elif inner.type == "function_definition" and name.startswith("test_"):
                    boundaries.append(
                        TestBoundary(
                            start_line=node.start_point[0] + 1,
                            end_line=node.end_point[0] + 1,
                            language="python",
                            pattern="test_function",
                        )
                    )

    boundaries.sort(key=lambda b: b.start_line)
    return tuple(boundaries)


def _extract_name(node) -> str:
    """Extract the identifier name from a class/function node."""
    for child in node.children:
        if child.type == "identifier":
            text = child.text
            if text is None:
                return ""
            return text.decode("utf-8") if isinstance(text, bytes) else text
    return ""


def _get_decorated_inner(node):
    """Get the class/function inside a decorated_definition."""
    for child in node.children:
        if child.type in ("class_definition", "function_definition"):
            return child
    return None
