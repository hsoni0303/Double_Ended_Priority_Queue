"""Small walkthrough of the double-ended priority queue."""

from depq import DoubleEndedPriorityQueue


def main() -> None:
    q = DoubleEndedPriorityQueue([42, 7, 19, 3, 88, 25])
    print(q)
    print(f"min={q.min()}  max={q.max()}  size={len(q)}")

    print("pop_min ->", q.pop_min())
    print("pop_max ->", q.pop_max())
    print(q)

    # Example use: keep only the 3 largest values from a stream.
    top3 = DoubleEndedPriorityQueue()
    for x in [5, 1, 9, 3, 12, 7, 2, 15]:
        top3.push(x)
        if len(top3) > 3:
            top3.pop_min()
    print("top 3 of stream:", sorted([top3.pop_max() for _ in range(len(top3))]))


if __name__ == "__main__":
    main()
