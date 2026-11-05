"""Array-backed binary heap whose entries know their own position.

Tracking each entry's index lets us delete an arbitrary entry in O(log n),
which the dual-heap DEPQ needs to remove an element's partner from the
other heap.
"""

from __future__ import annotations

import operator
from typing import Any, Callable, Generic, List, Optional, TypeVar

T = TypeVar("T")


class Entry(Generic[T]):
    """A value stored in one heap, linked to its partner in the other heap."""

    __slots__ = ("value", "index", "partner")

    def __init__(self, value: T) -> None:
        self.value = value
        self.index = -1
        self.partner: Optional[Entry[T]] = None

    def __repr__(self) -> str:
        return f"Entry({self.value!r})"


class IndexedHeap(Generic[T]):
    """Binary heap ordered by ``higher_priority(a, b)``.

    ``operator.lt`` gives a min-heap, ``operator.gt`` a max-heap.
    """

    def __init__(self, higher_priority: Callable[[Any, Any], bool]) -> None:
        self._items: List[Entry[T]] = []
        self._before = higher_priority

    def __len__(self) -> int:
        return len(self._items)

    def peek(self) -> Entry[T]:
        if not self._items:
            raise IndexError("peek from empty heap")
        return self._items[0]

    def push(self, entry: Entry[T]) -> None:
        entry.index = len(self._items)
        self._items.append(entry)
        self._sift_up(entry.index)

    def pop(self) -> Entry[T]:
        return self.remove(self.peek())

    def remove(self, entry: Entry[T]) -> Entry[T]:
        """Remove ``entry`` from anywhere in the heap in O(log n)."""
        i = entry.index
        if not (0 <= i < len(self._items)) or self._items[i] is not entry:
            raise ValueError(f"{entry!r} is not in this heap")

        last = self._items.pop()
        if last is not entry:
            # Move the last leaf into the hole, then restore heap order.
            self._items[i] = last
            last.index = i
            self._sift_up(i)
            self._sift_down(last.index)
        entry.index = -1
        return entry

    def values(self) -> List[T]:
        """Values in level order (array order)."""
        return [e.value for e in self._items]

    # -- internals ---------------------------------------------------------

    def _swap(self, i: int, j: int) -> None:
        items = self._items
        items[i], items[j] = items[j], items[i]
        items[i].index = i
        items[j].index = j

    def _sift_up(self, i: int) -> None:
        while i > 0:
            parent = (i - 1) // 2
            if not self._before(self._items[i].value, self._items[parent].value):
                break
            self._swap(i, parent)
            i = parent

    def _sift_down(self, i: int) -> None:
        n = len(self._items)
        while True:
            best = i
            for child in (2 * i + 1, 2 * i + 2):
                if child < n and self._before(
                    self._items[child].value, self._items[best].value
                ):
                    best = child
            if best == i:
                return
            self._swap(i, best)
            i = best


def min_heap() -> IndexedHeap:
    return IndexedHeap(operator.lt)


def max_heap() -> IndexedHeap:
    return IndexedHeap(operator.gt)
