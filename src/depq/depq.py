"""Double-ended priority queue built from two corresponding heaps.

Elements are grouped into pairs ``(small, large)``. The smaller element of
each pair lives in a min-heap, the larger in a max-heap, and the two entries
point at each other. With an odd number of elements, one extra element sits
in a single-slot ``buffer``.

Invariant: for every pair, ``small <= large``. Therefore the global minimum
is either the min-heap root or the buffer, and the global maximum is either
the max-heap root or the buffer.
"""

from __future__ import annotations

from typing import Generic, Iterable, Optional, TypeVar

from .heap import Entry, IndexedHeap, max_heap, min_heap

T = TypeVar("T")

_EMPTY = object()


class DoubleEndedPriorityQueue(Generic[T]):
    """Supports O(1) ``min``/``max`` and O(log n) ``push``/``pop_min``/``pop_max``."""

    def __init__(self, items: Optional[Iterable[T]] = None) -> None:
        self._min: IndexedHeap[T] = min_heap()
        self._max: IndexedHeap[T] = max_heap()
        self._buffer = _EMPTY
        for item in items or ():
            self.push(item)

    # -- size ----------------------------------------------------------------

    def __len__(self) -> int:
        return 2 * len(self._min) + (self._buffer is not _EMPTY)

    def __bool__(self) -> bool:
        return len(self) > 0

    # -- queries -------------------------------------------------------------

    def min(self) -> T:
        self._require_nonempty()
        if self._buffer_wins(self._min, lambda b, top: b <= top):
            return self._buffer  # type: ignore[return-value]
        return self._min.peek().value

    def max(self) -> T:
        self._require_nonempty()
        if self._buffer_wins(self._max, lambda b, top: b >= top):
            return self._buffer  # type: ignore[return-value]
        return self._max.peek().value

    # -- updates -------------------------------------------------------------

    def push(self, value: T) -> None:
        if self._buffer is _EMPTY:
            self._buffer = value
            return
        partner, self._buffer = self._buffer, _EMPTY
        self._add_pair(value, partner)  # type: ignore[arg-type]

    def pop_min(self) -> T:
        self._require_nonempty()
        if self._buffer_wins(self._min, lambda b, top: b <= top):
            return self._take_buffer()
        return self._pop_pair_end(self._min, self._max)

    def pop_max(self) -> T:
        self._require_nonempty()
        if self._buffer_wins(self._max, lambda b, top: b >= top):
            return self._take_buffer()
        return self._pop_pair_end(self._max, self._min)

    def replace_min(self, value: T) -> T:
        """Pop the minimum and push ``value``; returns the popped minimum."""
        smallest = self.pop_min()
        self.push(value)
        return smallest

    # -- internals -------------------------------------------------------------

    def _add_pair(self, a: T, b: T) -> None:
        small, large = (a, b) if a <= b else (b, a)
        lo, hi = Entry(small), Entry(large)
        lo.partner, hi.partner = hi, lo
        self._min.push(lo)
        self._max.push(hi)

    def _pop_pair_end(self, own: IndexedHeap[T], other: IndexedHeap[T]) -> T:
        """Pop ``own``'s root, delete its partner from ``other``, and
        re-insert the orphaned partner (pairing it with the buffer if any)."""
        top = own.pop()
        orphan = other.remove(top.partner)  # type: ignore[arg-type]
        self.push(orphan.value)
        return top.value

    def _buffer_wins(self, heap: IndexedHeap[T], beats) -> bool:
        if self._buffer is _EMPTY:
            return False
        return len(heap) == 0 or beats(self._buffer, heap.peek().value)

    def _take_buffer(self) -> T:
        value, self._buffer = self._buffer, _EMPTY
        return value  # type: ignore[return-value]

    def _require_nonempty(self) -> None:
        if not self:
            raise IndexError("double-ended priority queue is empty")

    def __repr__(self) -> str:
        buf = None if self._buffer is _EMPTY else self._buffer
        return (
            f"DoubleEndedPriorityQueue(min_heap={self._min.values()}, "
            f"max_heap={self._max.values()}, buffer={buf!r})"
        )
