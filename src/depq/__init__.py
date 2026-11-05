"""Double-ended priority queue using corresponding min/max heaps."""

from .depq import DoubleEndedPriorityQueue
from .heap import IndexedHeap, max_heap, min_heap

__all__ = ["DoubleEndedPriorityQueue", "IndexedHeap", "min_heap", "max_heap"]
__version__ = "1.0.0"
