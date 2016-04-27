from collections import deque


class CircularBuffer(deque):
    def __init__(self, size=0):
        super(CircularBuffer, self).__init__(maxlen=size)

    @property
    def average(self):
        return sum(self) / len(self)
