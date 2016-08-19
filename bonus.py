from random import randrange
from constants import *

class Bonus(object):
    def __init__(self, stdscr, kind=0):
    
        self.x = randrange(1, MAX_WIDTH-1)
        self.y = randrange(1, MAX_HEIGHT-1)
        while stdscr.inch(self.y, self.x) != 32:
            self.x = randrange(1, MAX_WIDTH-1)
            self.y = randrange(1, MAX_HEIGHT-1)
        self.kind = kind
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getKind(self):
        return self.kind

