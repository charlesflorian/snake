from queue import Queue
from constants import *
from exceptions import *

class Snake(object):

    def __init__(self, stdscr, l=3, d=3, x=MAX_WIDTH/2, y=MAX_HEIGHT/2):
        self.stdscr = stdscr #Need this for collision detection, I guess?
        self.l = l
        self.next_direction = d
        self.cur_direction = self.next_direction
        self.x = x
        self.y = y
        
        self.score = 0
        
        self.Q = Queue()
        self.Q.enqueue((x,y))
            
    def setDirection(self, direction):
        """
        N = 0
        E = 1
        S = 2
        W = 3
        
        """
        if direction > DIR_WEST or direction < DIR_NORTH:
            raise Exception("Invalid Direction: " + str(direction))
        
        if (self.cur_direction + direction) % 2 != 0: # This should work...
            self.next_direction = direction
    
    def getNextDirection(self):
        return self.next_direction
    
    def getCurrentDirection(self):
        return self.cur_direction
    
    def getScore(self):
        return self.score
    
    def addToScore(self, amount):
        self.score += amount
    
    def getLength(self):
        return self.l
    
    def lengthen(self):
        self.l *= 1.5
    
    def __iter__(self):
        return self.Q.__iter__()
    
    def collision(self, x, y):
        c = self.stdscr.inch(y, x)
        if c != BLANK_SQUARE:
            if c == BONUS:
                # Get longer!
                raise BonusException()
            else:
                raise CollisionException()
        return False
    
    def move(self):
        if self.getNextDirection() == DIR_NORTH:
            self.cur_direction = DIR_NORTH
            self.y -= 1
            self.Q.enqueue((self.x, self.y))
            if self.Q.size() > self.getLength():
                self.Q.dequeue()
        elif self.getNextDirection() == DIR_EAST:
            self.cur_direction = DIR_EAST
            self.x += 1
            self.Q.enqueue((self.x, self.y))
            if self.Q.size() > self.getLength():
                self.Q.dequeue()
        elif self.getNextDirection() == DIR_SOUTH:
            self.cur_direction = DIR_SOUTH
            self.y += 1
            self.Q.enqueue((self.x, self.y))
            if self.Q.size() > self.getLength():
                self.Q.dequeue()
        elif self.getNextDirection() == DIR_WEST:
            self.cur_direction = DIR_WEST
            self.x -= 1
            self.Q.enqueue((self.x, self.y))
            if self.Q.size() > self.getLength():
                self.Q.dequeue()
        
        self.collision(self.x, self.y)
            
        return (self.x, self.y)

