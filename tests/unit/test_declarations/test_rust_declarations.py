"""Unit tests for Rust declaration detection."""

from __future__ import annotations

import textwrap

from eigenhelm.declarations.models import DeclarationType
from eigenhelm.declarations.rust import detect


class TestConstTable:
    """const/static arrays of struct literals -> CONST_TABLE."""

    def test_const_array_of_struct_literals(self):
        src = textwrap.dedent("""\
            const ITEMS: [Item; 2] = [
                Item { name: "a", val: 1 },
                Item { name: "b", val: 2 },
            ];
        """)
        regions = detect(src)
        assert len(regions) == 1
        r = regions[0]
        assert r.declaration_type == DeclarationType.CONST_TABLE
        assert r.node_name == "ITEMS"
        assert r.language == "rust"

    def test_static_array_of_struct_literals(self):
        src = textwrap.dedent("""\
            static ROUTES: [Route; 1] = [
                Route { path: "/home", handler: home },
            ];
        """)
        regions = detect(src)
        assert len(regions) == 1
        assert regions[0].declaration_type == DeclarationType.CONST_TABLE
        assert regions[0].node_name == "ROUTES"


class TestStructDefinition:
    """struct definitions -> TYPE_DEFINITION."""

    def test_struct_detected_as_type_definition(self):
        src = textwrap.dedent("""\
            struct Point {
                x: f64,
                y: f64,
            }
        """)
        regions = detect(src)
        assert len(regions) == 1
        r = regions[0]
        assert r.declaration_type == DeclarationType.TYPE_DEFINITION
        assert r.node_name == "Point"
        assert r.start_line == 1
        assert r.end_line == 4

    def test_struct_with_impl_block_only_detects_struct(self):
        src = textwrap.dedent("""\
            struct Rect {
                w: f64,
                h: f64,
            }

            impl Rect {
                fn area(&self) -> f64 {
                    self.w * self.h
                }
            }
        """)
        regions = detect(src)
        assert len(regions) == 1
        r = regions[0]
        assert r.declaration_type == DeclarationType.TYPE_DEFINITION
        assert r.node_name == "Rect"
        # Only the struct lines, not the impl block
        assert r.start_line == 1
        assert r.end_line == 4


class TestEnumDeclaration:
    """Value-only enums -> ENUM_DECLARATION; data-carrying enums -> not detected."""

    def test_value_only_enum_detected(self):
        src = textwrap.dedent("""\
            enum Color {
                Red,
                Green,
                Blue,
            }
        """)
        regions = detect(src)
        assert len(regions) == 1
        r = regions[0]
        assert r.declaration_type == DeclarationType.ENUM_DECLARATION
        assert r.node_name == "Color"

    def test_enum_with_tuple_variant_not_detected(self):
        src = textwrap.dedent("""\
            enum Shape {
                Circle(f64),
                Square(f64),
            }
        """)
        regions = detect(src)
        assert len(regions) == 0

    def test_enum_with_impl_block_only_detects_enum(self):
        src = textwrap.dedent("""\
            enum Direction {
                North,
                South,
                East,
                West,
            }

            impl Direction {
                fn opposite(&self) -> Direction {
                    match self {
                        Direction::North => Direction::South,
                        Direction::South => Direction::North,
                        Direction::East => Direction::West,
                        Direction::West => Direction::East,
                    }
                }
            }
        """)
        regions = detect(src)
        assert len(regions) == 1
        r = regions[0]
        assert r.declaration_type == DeclarationType.ENUM_DECLARATION
        assert r.node_name == "Direction"
        assert r.end_line == 6


class TestNotDetected:
    """Constructs that should NOT produce any regions."""

    def test_function_not_detected(self):
        src = textwrap.dedent("""\
            fn add(a: i32, b: i32) -> i32 {
                a + b
            }
        """)
        regions = detect(src)
        assert len(regions) == 0


class TestEmptySource:
    """Edge case: empty input."""

    def test_empty_source_returns_empty_tuple(self):
        assert detect("") == ()
