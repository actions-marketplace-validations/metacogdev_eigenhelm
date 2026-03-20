"""Go declaration detection via tree-sitter.

Detects type struct definitions, const iota blocks, and var blocks
with struct literal arrays.
"""

from __future__ import annotations

from eigenhelm.declarations.models import DeclarationRegion, DeclarationType


def detect(source: str) -> tuple[DeclarationRegion, ...]:
    """Detect Go declaration constructs.

    Finds:
    - type struct definitions (TYPE_DEFINITION)
    - const iota blocks (ENUM_DECLARATION)
    - var blocks with composite struct literals (CONST_TABLE)

    Does NOT detect function declarations, method declarations,
    or interface types.

    Returns:
        Sorted DeclarationRegion entries by start_line.
    """
    from eigenhelm.parsers.tree_sitter import parse_source

    root = parse_source(source, "go")
    if root is None:
        return ()

    regions: list[DeclarationRegion] = []
    source_lines = source.splitlines()

    for node in root.children:
        if node.type == "type_declaration":
            _handle_type_declaration(node, source_lines, regions)
        elif node.type == "const_declaration":
            _handle_const_declaration(node, source_lines, regions)
        elif node.type == "var_declaration":
            _handle_var_declaration(node, source_lines, regions)

    regions.sort(key=lambda r: r.start_line)
    return tuple(regions)


def _handle_type_declaration(
    node, source_lines: list[str], regions: list[DeclarationRegion]
) -> None:
    """Process type_declaration nodes, emitting struct definitions."""
    for child in node.children:
        if child.type == "type_spec":
            if _has_struct_type(child):
                name = _extract_name(child)
                start = node.start_point[0] + 1
                end = node.end_point[0] + 1
                regions.append(
                    DeclarationRegion(
                        declaration_type=DeclarationType.TYPE_DEFINITION,
                        start_line=start,
                        end_line=end,
                        declaration_line_count=_count_non_blank(
                            source_lines, start, end
                        ),
                        language="go",
                        node_name=name,
                    )
                )


def _handle_const_declaration(
    node, source_lines: list[str], regions: list[DeclarationRegion]
) -> None:
    """Process const_declaration nodes as enum declarations.

    Only detects const blocks that contain iota or grouped const specs
    (parenthesized blocks), not standalone const assignments.
    """
    if not _is_iota_or_grouped_const(node):
        return

    name = _const_block_name(node)
    start = node.start_point[0] + 1
    end = node.end_point[0] + 1
    regions.append(
        DeclarationRegion(
            declaration_type=DeclarationType.ENUM_DECLARATION,
            start_line=start,
            end_line=end,
            declaration_line_count=_count_non_blank(source_lines, start, end),
            language="go",
            node_name=name,
        )
    )


def _is_iota_or_grouped_const(node) -> bool:
    """Check if const block uses iota or is a grouped (parenthesized) block."""
    text = node.text
    if text is None:
        return False
    decoded = text.decode("utf-8") if isinstance(text, bytes) else text
    # Grouped const blocks contain parentheses; iota blocks contain "iota"
    return "iota" in decoded or ("(" in decoded and ")" in decoded)


def _handle_var_declaration(
    node, source_lines: list[str], regions: list[DeclarationRegion]
) -> None:
    """Process var_declaration nodes with composite struct literal arrays."""
    if not _has_composite_struct_literal(node):
        return

    name = _var_block_name(node)
    start = node.start_point[0] + 1
    end = node.end_point[0] + 1
    regions.append(
        DeclarationRegion(
            declaration_type=DeclarationType.CONST_TABLE,
            start_line=start,
            end_line=end,
            declaration_line_count=_count_non_blank(source_lines, start, end),
            language="go",
            node_name=name,
        )
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _has_struct_type(type_spec_node) -> bool:
    """Check if a type_spec has a struct_type child."""
    for child in type_spec_node.children:
        if child.type == "struct_type":
            return True
    return False


def _has_composite_struct_literal(node) -> bool:
    """Check if a var_declaration contains a composite literal with struct literal elements.

    Requires the composite literal to contain at least one keyed_element
    (field: value pairs), which distinguishes struct literals from plain
    slice/map literals.
    """
    comp = _find_node_type(node, "composite_literal")
    if comp is None:
        return False
    # Check for keyed_element children (struct field initialization)
    return _find_node_type(comp, "keyed_element") is not None


def _find_node_type(node, target_type: str):
    """Recursively find a descendant node of the given type."""
    if node.type == target_type:
        return node
    for child in node.children:
        result = _find_node_type(child, target_type)
        if result is not None:
            return result
    return None


def _extract_name(node) -> str:
    """Extract the identifier name from a node."""
    for child in node.children:
        if child.type == "type_identifier" or child.type == "identifier":
            text = child.text
            if text is None:
                return ""
            return text.decode("utf-8") if isinstance(text, bytes) else text
    return ""


def _const_block_name(node) -> str:
    """Extract a representative name from a const block.

    Uses the first const_spec's identifier.
    """
    for child in node.children:
        if child.type == "const_spec":
            return _extract_name(child)
    return "const"


def _var_block_name(node) -> str:
    """Extract a representative name from a var block.

    Uses the first var_spec's identifier.
    """
    for child in node.children:
        if child.type == "var_spec":
            return _extract_name(child)
    return "var"


def _count_non_blank(source_lines: list[str], start: int, end: int) -> int:
    """Count non-blank lines within a 1-indexed line range (inclusive)."""
    count = 0
    for line in source_lines[start - 1 : end]:
        if line.strip():
            count += 1
    return max(count, 1)
