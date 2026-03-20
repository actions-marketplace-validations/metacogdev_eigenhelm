"""Rust test boundary detection via tree-sitter.

Detects #[cfg(test)] mod blocks and returns their line ranges.
"""

from __future__ import annotations

from eigenhelm.regions.models import TestBoundary


def detect(source: str) -> tuple[TestBoundary, ...]:
    """Detect Rust test module boundaries.

    Finds `#[cfg(test)] mod <name> { ... }` blocks by walking the AST
    for mod_item nodes preceded by a cfg(test) attribute.

    Returns:
        Sorted, non-overlapping TestBoundary entries.
    """
    from eigenhelm.parsers.tree_sitter import parse_source

    root = parse_source(source, "rust")
    if root is None:
        return ()

    boundaries: list[TestBoundary] = []

    for node in root.children:
        if node.type == "mod_item" and _has_cfg_test_attr(node):
            start_line = node.start_point[0] + 1  # 1-indexed
            end_line = node.end_point[0] + 1
            boundaries.append(
                TestBoundary(
                    start_line=start_line,
                    end_line=end_line,
                    language="rust",
                    pattern="cfg_test_module",
                )
            )

    boundaries.sort(key=lambda b: b.start_line)
    return tuple(boundaries)


def _has_cfg_test_attr(mod_node) -> bool:
    """Check if a mod_item is preceded by #[cfg(test)]."""
    # In Rust AST, attributes are sibling nodes before the mod_item,
    # or they may be children of the mod_item depending on tree-sitter version.
    # Check both the node's children and preceding siblings.

    # Check children (some tree-sitter versions nest attrs inside mod_item)
    for child in mod_node.children:
        if child.type == "attribute_item" and _is_cfg_test(child):
            return True

    # Check preceding siblings
    prev = mod_node.prev_sibling
    while prev is not None and prev.type == "attribute_item":
        if _is_cfg_test(prev):
            return True
        prev = prev.prev_sibling

    return False


def _is_cfg_test(attr_node) -> bool:
    """Check if an attribute_item is #[cfg(test)].

    Uses strict matching to avoid false positives on #[cfg(not(test))],
    #[cfg(feature = "contest")], etc.
    """
    text = attr_node.text
    if text is None:
        return False
    decoded = text.decode("utf-8") if isinstance(text, bytes) else text
    # Normalize all whitespace (spaces, tabs, newlines) for comparison
    normalized = "".join(decoded.split())
    return normalized == "#[cfg(test)]"
