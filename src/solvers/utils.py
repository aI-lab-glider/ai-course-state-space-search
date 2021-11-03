from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass
import heapq
from dataclasses import dataclass, field
from typing import Any, Callable, Deque, Generic, List, TypeVar


class Queue(ABC):
    @abstractmethod
    def push(self, x) -> None:
        pass 

    @abstractmethod
    def pop(self) -> Any:
        pass 

    @abstractmethod
    def is_empty(self) -> bool:
        pass

class FIFO(Queue):

    def __init__(self) -> None:
        self.queue: Deque = deque()
        super().__init__()

    def push(self, x) -> None:
        self.queue.append(x)
    
    def pop(self) -> Any:
        return self.queue.popleft()

    def is_empty(self) -> bool:
        return len(self.queue) == 0

class LIFO(Queue):

    def __init__(self) -> None:
        self.queue: Deque = deque()
        super().__init__()

    def push(self, x) -> None:
        self.queue.append(x)
    
    def pop(self) -> Any:
        return self.queue.pop()

    def is_empty(self) -> bool:
        return len(self.queue) == 0

@dataclass(order=True)
class PQItem():
    distance: int
    item: Any=field(compare=False)

class PriorityQueue(Queue):
       
    def __init__(self, key: Callable):
        self.key=key
        self.heap: List[PQItem] = []
        heapq.heapify(self.heap)

    def push(self, x: Any):
        heapq.heappush(self.heap, PQItem(self.key(x), x))

    def pop(self) -> Any:
        hitem = heapq.heappop(self.heap)
        return hitem.item
        
    def is_empty(self):
        return len(self.heap) == 0

