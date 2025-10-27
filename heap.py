# implemetnation ofa heap using fixed size array

class BoundedMaxHeap:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._a = [None] * capacity # fixed-sized backing array
        self._n = 0 # size
        self._cap = capacity

    # -- index helpers (for 0-based heap) --
    def _parent(self, i): return (i - 1) // 2
    def _left(self, i): return 2 * i + 1
    def _right(self, i): return 2 * i + 2
    
    # -- get/boolean functions
    def __len__(self): return self._n
    def capacity(self): return self._cap
    def is_empty(self): return self._n == 0
    def is_full(self): return self._n == self._cap

    def peek(self):
        if self._n == 0:
            raise IndexError("peek from empty heap")
        return self._a[0]

    def push(self, x):
        # Insert x; O(logn). Raises heap if full
        if self._n == self._cap:
            raise OverflowError("heap is full")
        i = self._n
        self._a[i] = x 
        self._n += 1
        self.go_up(i)

    def pop(self):
        if self._n == 0:
            raise IndexError("pop from empty heal")
        top = self._a[0]
        # move last to root and shrink
        self._n -= 1
        self._a[0] = self._a[self._n]
        self._a[self._n] = None # clear slot
        if self._n > 0:
            self.go_down(0)
        return top

    def construct(self, iterable):
        """
        Build from the iterable (up to capacity) in O(n)
        Overwrites values
        """
        self._n = 0
        for i, v in enumerate(iterable):
            if i == self._cap:
                break
            self._a[i] = v 
            self._n += 1
        # Bottom up heapify 
        for i in range((self._n // 2) - 1, -1, -1):
            self.go_down(i)
        # Clear leftover slots if iterable < capacity
        for i in range(self._n, self._cap):
            self._a[i] = None

    ## The heapify_up and heapify_down equivalents for Lab 3
    def go_up(self, i):
        while i > 0:
            p = self._parent(i)
            if self._a[p] >= self._a[i]:
                break
            self._a[p], self._a[i] = self._a[i], self._a[p]
            i = p
    ## Compare to left & right children until current idx val is 
    ## the largest or until at the bottom of the list
    def go_down(self, i):
        n = self._n
        while True:
            l, r = self._left(i), self._right(i)
            largest = i
            if l < n and self._a[l] > self._a[largest]:
                largest = l
            if r < n and self._a[r] > self._a[largest]:
                largest = r 
            if largest == i:
                break
            self._a[i], self._a[largest] = self._a[largest], self._a[i]
            i = largest
    # debug array
    def array(self):
        return self._a[:]

class Test:
    h = BoundedMaxHeap(10)
    h.push(10)
    h.push(4)
    h.push(22)
    h.push(7)
    print(h.peek()) # 22
    print(h.pop()) # 22
    print(h.__len__()) # 3
    print(h.peek()) # 10
    a = [3, 17, 8, 25, 1]
    print("Initial array: ", a)
    h.construct(a)
    print("After heap construction: ", h.array())
