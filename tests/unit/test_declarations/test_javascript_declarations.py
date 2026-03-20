"""Unit tests for JavaScript declaration detection."""

from __future__ import annotations

from eigenhelm.declarations.models import DeclarationType
from eigenhelm.declarations.javascript import detect


class TestConstTable:
    def test_const_array_of_objects_detected(self) -> None:
        source = """\
const COLORS = [
  { name: "red", hex: "#ff0000" },
  { name: "green", hex: "#00ff00" },
];
"""
        regions = detect(source)
        assert len(regions) == 1
        assert regions[0].declaration_type == DeclarationType.CONST_TABLE
        assert regions[0].node_name == "COLORS"
        assert regions[0].language == "javascript"

    def test_exported_const_table_detected(self) -> None:
        source = """\
export const ENDPOINTS = [
  { method: "GET", path: "/api/users" },
  { method: "POST", path: "/api/users" },
];
"""
        regions = detect(source)
        assert len(regions) == 1
        assert regions[0].declaration_type == DeclarationType.CONST_TABLE

    def test_let_array_not_detected(self) -> None:
        source = """\
let items = [
  { id: 1 },
  { id: 2 },
];
"""
        regions = detect(source)
        assert len(regions) == 0

    def test_const_primitive_array_not_detected(self) -> None:
        source = """\
const NUMBERS = [1, 2, 3, 4, 5];
"""
        regions = detect(source)
        assert len(regions) == 0


class TestFieldOnlyClass:
    def test_field_only_class_detected(self) -> None:
        source = """\
class Config {
  host = "localhost";
  port = 8080;
  debug = false;
}
"""
        regions = detect(source)
        assert len(regions) == 1
        assert regions[0].declaration_type == DeclarationType.FIELD_ONLY_CLASS
        assert regions[0].node_name == "Config"


class TestClassWithMethodsNotDetected:
    def test_class_with_methods_not_detected(self) -> None:
        source = """\
class Service {
  url = "/api";

  fetch() {
    return null;
  }
}
"""
        regions = detect(source)
        assert len(regions) == 0

    def test_class_with_only_methods_not_detected(self) -> None:
        source = """\
class Calculator {
  add(a, b) {
    return a + b;
  }
  subtract(a, b) {
    return a - b;
  }
}
"""
        regions = detect(source)
        assert len(regions) == 0


class TestFunctionNotDetected:
    def test_function_declaration_not_detected(self) -> None:
        source = """\
function greet(name) {
  return "Hello, " + name;
}
"""
        regions = detect(source)
        assert len(regions) == 0

    def test_arrow_function_not_detected(self) -> None:
        source = """\
const add = (a, b) => a + b;
"""
        regions = detect(source)
        assert len(regions) == 0


class TestEmptySource:
    def test_empty_string_returns_empty(self) -> None:
        assert detect("") == ()

    def test_whitespace_only_returns_empty(self) -> None:
        assert detect("   \n\n  ") == ()
