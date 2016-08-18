class iterQueue:
    def __init__(self, items):
        self.items = items
        self.idx = len(self.items)
    
    def next(self):
        if self.idx > 0:
            self.idx -= 1
            return self.items[self.idx]
        else:
            raise StopIteration()

class Queue:
    def __init__(self):
        self.items = []
    
    def isEmpty(self):
        return len(self.items) == 0
    
    def enqueue(self, item):
        self.items.insert(0, item)
    
    def dequeue(self):
        return self.items.pop()
     
    def size(self):
        return len(self.items)
        
    def peek(self):
        return self.items[-1]
        
    def __iter__(self):
        return iterQueue(self.items[:])

if __name__ == '__main__':    
    # Unit tests, baby!
    q = Queue()
    for i in range(10):
        q.enqueue(i)
    print q.dequeue()
    print q.dequeue()
    q.enqueue(55)
    for j in q:
        print j
