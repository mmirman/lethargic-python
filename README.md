Lethargic Python
================

Lethargic Python is a library for creating non-strict, semi-lazy thunks. Unlike usual lazy semantics, only a predetermined number of thunks can be created before they will start being evaluated in a FIFO manner. This obliterates the usual complaint with lazy semantics that it is easier to create space leaks wherean unbounded number of thunks can be created.  Now, you'll be forced to think your code through as your thunk queue is finite.

Features & Advantages
---------------------

* Only finite number of delayed thunks can be created.

* Thunks can be garbage collected as is usual.

* Thunks get evaluated in a FIFO manner.

* Space leaks become time leaks: much easier to reason about.

Wear Goggles in The Lab
-----------------------

* Doing this right involves some care to ensure that thunks which are no longer needed get garbage collected.  

Workings
--------

* Each new thunk object is also a node in a doubly linked queue list.

* When a thunk gets created, a thunk node added to the queue with a weak reference to the thunk which executes a removal callback upon being collected which removes the object from the queue.

* If the queue is too large, pop thunks off the queue and evaluate them.

* when a thunk gets forced, remove it from the queue (one of two reasons the queue is doubly linked)

Usage
-----

```python
import lethargy

lazy = lethargy.lethargy(3)

def test(a):
    print a

for i in xrange(3):
    a = lazy.delay(test,i)
a()  # prints 2
a()  # does nothing

a = lazy.delay(test,'a') # no output
b = lazy.delay(test,'b') # no output

print "LADIES AND GENTLEMEN: "

c = lazy.delay(test,'c') # prints a
d = lazy.delay(test,'d') # prints b

def hold():
    a()
    b()
    c()
```

This should print:

```
2
LADIES AND GENTLEMEN: 
a
b
```

Author
------

* Matthew Mirman ( mmirman@andrew.cmu.edu )


License
-------

See LICENSE file.