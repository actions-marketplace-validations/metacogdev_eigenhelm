"""Pure test file — no production code."""

import unittest


class TestMathOperations(unittest.TestCase):
    def test_addition(self):
        assert 1 + 1 == 2

    def test_subtraction(self):
        assert 5 - 3 == 2

    def test_multiplication(self):
        assert 3 * 4 == 12

    def test_division(self):
        assert 10 / 2 == 5.0

    def test_integer_division(self):
        assert 7 // 2 == 3

    def test_modulo(self):
        assert 10 % 3 == 1


class TestStringOperations(unittest.TestCase):
    def test_concat(self):
        assert "hello" + " " + "world" == "hello world"

    def test_upper(self):
        assert "hello".upper() == "HELLO"

    def test_split(self):
        assert "a,b,c".split(",") == ["a", "b", "c"]


def test_standalone_bool():
    assert bool(1) is True
    assert bool(0) is False
