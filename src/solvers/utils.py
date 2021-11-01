from dataclasses import dataclass
import heapq
from dataclasses import dataclass, field
from typing import Any, Callable, List

@dataclass(order=True)
class HeapItem:
    distance: int
    item: Any=field(compare=False)

class Heap:
       
    def __init__(self, key: Callable):
        self.key=key
        self.heap: List[HeapItem] = []
        heapq.heapify(self.heap)

    def push(self, x):
        heapq.heappush(self.heap, HeapItem(self.key(x), x))

    def pop(self):
        hitem = heapq.heappop(self.heap)
        return hitem.item
        
    def is_empty(self):
        return len(self.heap) == 0