import weakref



class TQ:
    head = None
    tail = None
    size = 0
    
    def qsize(self):
        return self.size

    def put(self,item):
        item.next = self.head
        item.prev = None
        self.head = item

        self.size += 1

        if item.next:
            item.next.prev = self.head
        else: 
            self.tail = self.head
            
        item.enqueued = True

    def get_nowait(self):
        if not self.tail:
            return None
        old_tail = self.tail
        self.size -= 1
        self.tail = old_tail.prev
        old_tail.prev = None

        if self.tail:
            self.tail.next = None
        else: 
            self.head = None

        old_tail.enqueued = False

        return old_tail

    def remove(self,item):
        if not item.enqueued:
            return

        self.size -= 1
        
        if item.prev:
            item.prev.next = item.next
        else: 
            self.head = item.next

        if item.next:
            item.next.prev = item.prev
        else:
            self.tail = item.prev

        item.prev = None
        item.next = None
        item.enqueued = False



class Lazy(object):
    next = None
    prev = None
    enqueued = False
    
    def __init__(self, lethargy, foo, *args, **kargs):
        self.lethargy = lethargy
        self.foo = foo
        self.args = args
        self.kargs = kargs

    def force(self):
        return self.defer()

    def defer(self):
        self.lethargy.thunk_queue.remove(self)
        
        forced = self.foo(*self.args, **self.kargs)
        def done():
            return forced
        
        self.defer = done
        
        return forced

class lethargy(object):


    thunk_queue = TQ()

    def __init__(self, max_waiting_thunks = 3):
        self.max_waiting_thunks = max_waiting_thunks

    def delay(self, foo, *args, **kargs):
        thunk = Lazy(self, foo, *args, **kargs)

        thunk_forcer = thunk.force

        def finalize_and_remove(s):
            if thunk and thunk.enqueued:
                self.thunk_queue.remove(thunk)

        thunk.force = weakref.ref(thunk_forcer, finalize_and_remove)
        self.thunk_queue.put(thunk)

        while self.thunk_queue.qsize() >= self.max_waiting_thunks:
            t = self.thunk_queue.get_nowait()
            if t and t.force:
                t = t.force()
                if t:
                    t()

        return thunk_forcer
