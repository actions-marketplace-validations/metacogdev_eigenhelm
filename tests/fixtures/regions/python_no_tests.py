"""A simple counter module with no test code."""


class Counter:
    """Thread-unsafe counter for demonstration."""

    def __init__(self, initial=0):
        self._value = initial

    def increment(self, amount=1):
        self._value += amount

    def decrement(self, amount=1):
        self._value -= amount

    def reset(self):
        self._value = 0

    @property
    def value(self):
        return self._value

    def __repr__(self):
        return f"Counter({self._value})"


def make_counter(initial=0):
    """Factory function for Counter instances."""
    return Counter(initial)
