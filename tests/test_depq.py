import random

import pytest

from depq import DoubleEndedPriorityQueue, max_heap, min_heap
from depq.heap import Entry


def test_empty_queue_raises():
    q = DoubleEndedPriorityQueue()
    assert len(q) == 0 and not q
    for op in (q.min, q.max, q.pop_min, q.pop_max):
        with pytest.raises(IndexError):
            op()


def test_single_element_is_both_min_and_max():
    q = DoubleEndedPriorityQueue([7])
    assert q.min() == q.max() == 7
    assert q.pop_max() == 7
    assert not q


def test_basic_ordering():
    q = DoubleEndedPriorityQueue([5, 1, 9, 3, 7])
    assert (q.min(), q.max()) == (1, 9)
    assert q.pop_min() == 1
    assert q.pop_max() == 9
    assert q.pop_min() == 3
    assert q.pop_max() == 7
    assert q.pop_min() == 5
    assert len(q) == 0


def test_duplicates():
    q = DoubleEndedPriorityQueue([4, 4, 4, 2, 2])
    assert [q.pop_min() for _ in range(5)] == [2, 2, 4, 4, 4]


def test_replace_min():
    q = DoubleEndedPriorityQueue([3, 8, 5])
    assert q.replace_min(10) == 3
    assert (q.min(), q.max()) == (5, 10)


@pytest.mark.parametrize("seed", range(20))
def test_matches_sorted_list_reference(seed):
    rng = random.Random(seed)
    q = DoubleEndedPriorityQueue()
    ref = []
    for _ in range(500):
        op = rng.random()
        if op < 0.5 or not ref:
            x = rng.randint(-50, 50)
            q.push(x)
            ref.append(x)
            ref.sort()
        elif op < 0.75:
            assert q.pop_min() == ref.pop(0)
        else:
            assert q.pop_max() == ref.pop()
        assert len(q) == len(ref)
        if ref:
            assert (q.min(), q.max()) == (ref[0], ref[-1])


def test_indexed_heap_arbitrary_removal():
    h = min_heap()
    entries = [Entry(v) for v in [9, 2, 7, 4, 1, 8]]
    for e in entries:
        h.push(e)
    h.remove(entries[2])  # remove 7 from the middle
    assert [h.pop().value for _ in range(len(h))] == [1, 2, 4, 8, 9]


def test_indexed_heap_rejects_foreign_entry():
    h = max_heap()
    h.push(Entry(1))
    with pytest.raises(ValueError):
        h.remove(Entry(1))
