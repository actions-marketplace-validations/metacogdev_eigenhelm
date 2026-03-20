"""A simple stack implementation with interleaved test code."""

from collections import deque


class Stack:
    """A bounded stack with peek and size operations."""

    def __init__(self, max_size=100):
        self._items = deque(maxlen=max_size)
        self._max_size = max_size

    def push(self, item):
        if len(self._items) >= self._max_size:
            raise OverflowError("Stack is full")
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def clear(self):
        self._items.clear()


class TestStack:
    """Tests for Stack."""

    def test_push_and_pop(self):
        s = Stack()
        s.push(1)
        s.push(2)
        assert s.pop() == 2
        assert s.pop() == 1

    def test_peek(self):
        s = Stack()
        s.push(42)
        assert s.peek() == 42
        assert s.size() == 1

    def test_is_empty(self):
        s = Stack()
        assert s.is_empty()
        s.push(1)
        assert not s.is_empty()

    def test_size(self):
        s = Stack()
        assert s.size() == 0
        s.push(1)
        s.push(2)
        assert s.size() == 2

    def test_clear(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.clear()
        assert s.is_empty()


def test_stack_overflow():
    s = Stack(max_size=2)
    s.push(1)
    s.push(2)
    try:
        s.push(3)
        assert False, "Should have raised"
    except OverflowError:
        pass


def test_empty_pop():
    s = Stack()
    try:
        s.pop()
        assert False, "Should have raised"
    except IndexError:
        pass
