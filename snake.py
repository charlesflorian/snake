import curses
from time import sleep
import event
from queue import Queue
from random import randrange
from lvlfile import LvlFile

DIR_NORTH = 0
DIR_EAST  = 1
DIR_SOUTH = 2
DIR_WEST  = 3

FRAME_DELAY = 0.01
FRAME_LENGTH = 5

BLANK_SQUARE = 32
BONUS = ord('X')

MAX_WIDTH = 80
MAX_HEIGHT = 24

class CollisionException(Exception):
    pass
    
class BonusException(Exception):
    pass

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
                raise BonusException
            else:
                raise CollisionException
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

def drawBorder(stdscr):
    stdscr.border()

def drawSnake(snake, stdscr):
    for p in snake:
        stdscr.move(p[1], p[0])
        stdscr.addstr("o")
        #write(stdscr, str(p))

def drawBonus(bonus, stdscr):
    stdscr.move(bonus.y, bonus.x)
    stdscr.addstr("X")

def drawLevel(level, stdscr):
    for j in range(0, MAX_HEIGHT):
        for i in range(0, MAX_WIDTH):
            t = level.getTile(i, j)
            if t > 0:
                stdscr.move(j, i)
                stdscr.addch(t)
    
def draw(snake, bonus, level, stdscr):
    stdscr.clear()
    drawBorder(stdscr)
    drawSnake(snake, stdscr)
    drawBonus(bonus, stdscr)
    drawLevel(level, stdscr)
#    write(stdscr, "%d" % level.getTile(0,0), 0, 0)
    write(stdscr, "Score:%d" % snake.getScore(), 5, 0)
    stdscr.refresh()

def write(stdscr, string, x=1, y=1):
    stdscr.move(y,x)
    stdscr.addstr(string)

def playSnake(stdscr):
    curses.curs_set(0) # Hide the cursor!
    S = Snake(stdscr, l=4)
    
    B = Bonus(stdscr)
    
    L = LvlFile(0)
        
    draw(S, B, L, stdscr)    
        
    num_frames = 0
    frame_so_far = 0.0

    stdscr.nodelay(1)    
    while True:
        c = stdscr.getch()
        if c != -1:
            # So something actually happened...
            if c == ord('q'):
                break
            elif c == curses.KEY_UP:
                S.setDirection(DIR_NORTH)
            elif c == curses.KEY_RIGHT:
                S.setDirection(DIR_EAST)
            elif c == curses.KEY_DOWN:
                S.setDirection(DIR_SOUTH)
            elif c == curses.KEY_LEFT:
                S.setDirection(DIR_WEST)
        sleep(FRAME_DELAY)
        frame_so_far += FRAME_DELAY
        if frame_so_far > FRAME_LENGTH * FRAME_DELAY:
            frame_so_far = 0.0
            num_frames += 1
            # S Should move now
            try:
                S.move()
            except CollisionException: # Hit something!
                break
            except BonusException:
                S.lengthen()
                B = Bonus(stdscr)
                S.addToScore(10)
            draw(S, B, L, stdscr)
        

def main():
    curses.wrapper(playSnake)
    print "You lose!"
    
main()