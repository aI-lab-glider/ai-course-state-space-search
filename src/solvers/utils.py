# TODO: Make heap class using heapq
class Heap:
    def __init__(self, elements=[], maxheap=True, key=lambda x: x): # defaultowo tworzy maxheap
        self.elements=elements
        self.key=key
        self.size=len(elements)
        self.maxheap=maxheap
        self.build_heap()

    def compare(self, x, y):
        if self.maxheap:
            return self.key(self.elements[x]) > self.key(self.elements[y])
        else:
            return self.key(self.elements[x]) < self.key(self.elements[y])

    def heapify(self, i):
        l = 2 * i + 1
        r = 2 * i + 2
        largest = i
        if l < self.size and self.compare(l,largest):
            largest = l
        if r < self.size and self.compare(r,largest):
            largest = r
        if largest != i:
            self.elements[i] , self.elements[largest] = self.elements[largest] , self.elements[i]
            self.heapify(largest)
    
    def build_heap(self):
        for i in range(self.size // 2 , -1 , -1):
            self.heapify(i)

    def put(self, x):
        self.size += 1
        self.elements.append(x)
        i = self.size - 1
        parent = (i-1)//2
        while parent >= 0 and self.compare(i,parent):
            self.elements[parent] , self.elements[i] = self.elements[i] , self.elements[parent]
            i = parent
            parent = (i-1)//2 

    def get(self):
        if(self.size == 0):
            return None
        x = self.elements[0]
        self.elements[0] = self.elements[self.size - 1]
        self.elements.pop()
        self.size -= 1
        self.heapify(0)
        return x
        
    def empty(self):
        return self.size == 0