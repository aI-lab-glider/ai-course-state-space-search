from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass
import heapq
from dataclasses import dataclass, field
from typing import Any, Callable, Deque, List, Generic, TypeVar


TItem = TypeVar('TItem')


class Queue(ABC, Generic[TItem]):
    @abstractmethod
    def push(self, x: TItem) -> None:
        pass

    @abstractmethod
    def pop(self) -> TItem:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass


class FIFO(Queue[TItem]):
    """
    Implementation of First In First Out queue.

    Example: 

    >>> a = FIFO()
    >>> a.push(1)
    >>> a.push(2)
    >>> a.pop()
    1
    >>> a.pop()
    2    
    """

    def __init__(self) -> None:
        self.queue: Deque = deque()
        super().__init__()

    def push(self, x) -> None:
        self.queue.append(x)

    def pop(self) -> Any:
        return self.queue.popleft()

    def is_empty(self) -> bool:
        return len(self.queue) == 0


class LIFO(Queue[TItem]):
    """
    Implementation of Last In First Out queue.

    Example:

    >>> a = LIFO()
    >>> a.push(1)
    >>> a.push(2)
    >>> a.pop()
    2
    >>> a.pop()                                                                                                             
    1  
    """

    def __init__(self) -> None:
        self.queue: Deque = deque()
        super().__init__()

    def push(self, x) -> None:
        self.queue.append(x)

    def pop(self) -> TItem:
        return self.queue.pop()

    def is_empty(self) -> bool:
        return len(self.queue) == 0


@dataclass(order=True)
class PQItem(Generic[TItem]):
    distance: int
    item: TItem = field(compare=False)


class PriorityQueue(Generic[TItem]):
    """
    Implementation of priority queue.
    Higher priority have item with smaller `key` value


    Example:

    >>> a = PriorityQueue(lambda x: x) # simply return an item as its cost
    >>> a.push(2) # item with higher key value
    >>> a.push(1)
    >>> a.pop()
    1
    >>> a.pop()
    2
    """

    def __init__(self, key: Callable, items: List[TItem] = None):
        self.key = key
        self.heap: List[PQItem] = []
        heapq.heapify(self.heap)
        if items:
            for item in items:
                self.push(item)

    def push(self, x: TItem):
        heapq.heappush(self.heap, PQItem(self.key(x), x))

    def pop(self) -> TItem:
        hitem = heapq.heappop(self.heap)
        return hitem.item

    def is_empty(self):
        return len(self.heap) == 0

    def __bool__(self):
        return not self.is_empty()
