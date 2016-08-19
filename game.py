import curses
from time import sleep
import event
from queue import Queue
from random import randrange
from lvlfile import LvlFile
from snake import Snake

from constants import *
from exceptions import *


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
