"""Unit tests for TypeScript declaration detection."""

from __future__ import annotations

from eigenhelm.declarations.models import DeclarationType
from eigenhelm.declarations.typescript import detect


class TestInterfaceDeclaration:
    def test_interface_detected_as_type_definition(self) -> None:
        source = """\
interface User {
  name: string;
  age: number;
}
"""
        regions = detect(source)
        assert len(regions) == 1
        assert regions[0].declaration_type == DeclarationType.TYPE_DEFINITION
        assert regions[0].node_name == "User"
        assert regions[0].language == "typescript"


class TestTypeAlias:
    def test_type_alias_detected_as_type_definition(self) -> None:
        source = """\
type Status = "active" | "inactive" | "pending";
"""
        regions = detect(source)
        assert len(regions) == 1
        assert regions[0].declaration_type == DeclarationType.TYPE_DEFINITION
        assert regions[0].node_name == "Status"

    def test_multiline_type_alias(self) -> None:
        source = """\
type Config = {
  host: string;
  port: number;
};
"""
        regions = detect(source)
        assert len(regions) == 1
        assert regions[0].declaration_type == DeclarationType.TYPE_DEFINITION


class TestEnumDeclaration:
    def test_enum_detected_as_enum_declaration(self) -> None:
        source = """\
enum Color {
  Red,
  Green,
  Blue,
}
"""
        regions = detect(source)
        assert len(regions) == 1
        assert regions[0].declaration_type == DeclarationType.ENUM_DECLARATION
        assert regions[0].node_name == "Color"

    def test_enum_with_string_values(self) -> None:
        source = """\
enum Direction {
  Up = "UP",
  Down = "DOWN",
}
"""
        regions = detect(source)
        assert len(regions) == 1
        assert regions[0].declaration_type == DeclarationType.ENUM_DECLARATION


class TestConstTable:
    def test_const_array_of_objects_detected(self) -> None:
        source = """\
const ROUTES = [
  { path: "/home", name: "Home" },
  { path: "/about", name: "About" },
];
"""
        regions = detect(source)
        assert len(regions) == 1
        assert regions[0].declaration_type == DeclarationType.CONST_TABLE
        assert regions[0].node_name == "ROUTES"

    def test_let_array_not_detected(self) -> None:
        source = """\
let items = [
  { id: 1 },
  { id: 2 },
];
"""
        regions = detect(source)
        assert len(regions) == 0


class TestExportWrapped:
    def test_exported_interface_detected(self) -> None:
        source = """\
export interface Props {
  title: string;
  count: number;
}
"""
        regions = detect(source)
        assert len(regions) == 1
        assert regions[0].declaration_type == DeclarationType.TYPE_DEFINITION
        assert regions[0].node_name == "Props"

    def test_exported_enum_detected(self) -> None:
        source = """\
export enum Level {
  Low,
  Medium,
  High,
}
"""
        regions = detect(source)
        assert len(regions) == 1
        assert regions[0].declaration_type == DeclarationType.ENUM_DECLARATION

    def test_exported_type_alias_detected(self) -> None:
        source = """\
export type ID = string | number;
"""
        regions = detect(source)
        assert len(regions) == 1
        assert regions[0].declaration_type == DeclarationType.TYPE_DEFINITION


class TestFunctionsNotDetected:
    def test_function_declaration_not_detected(self) -> None:
        source = """\
function greet(name: string): string {
  return `Hello, ${name}`;
}
"""
        regions = detect(source)
        assert len(regions) == 0

    def test_arrow_function_not_detected(self) -> None:
        source = """\
const add = (a: number, b: number): number => a + b;
"""
        regions = detect(source)
        assert len(regions) == 0


class TestMixedFile:
    def test_declarations_and_functions_mixed(self) -> None:
        source = """\
interface Config {
  host: string;
  port: number;
}

function createConfig(): Config {
  return { host: "localhost", port: 8080 };
}

enum Mode {
  Dev,
  Prod,
}

const handler = (req: Request) => req.body;
"""
        regions = detect(source)
        assert len(regions) == 2
        types = {r.declaration_type for r in regions}
        assert DeclarationType.TYPE_DEFINITION in types
        assert DeclarationType.ENUM_DECLARATION in types


class TestEmptySource:
    def test_empty_string_returns_empty(self) -> None:
        assert detect("") == ()

    def test_whitespace_only_returns_empty(self) -> None:
        assert detect("   \n\n  ") == ()
