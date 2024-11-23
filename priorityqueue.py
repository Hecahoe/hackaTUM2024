import heapq


class PriorityQueue:
    """
    simple priorityqueue because stupid python has no custom sorting
    values should be a dict, heap will be sorted by keys.
    """

    def __init__(self, values: dict):
        self.values = values
        self.queue = heapq.heapify([v for v in values.keys()])

    def get_smallest(self):
        if self.queue:
            return self.values[heapq.heappop(self.queue)]
        else:
            raise IndexError("Pop from an empty priority queue")

    def is_empty(self):
        if self.queue is None:
            return True
        return len(self.queue) == 0
