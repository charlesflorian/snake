"""
File format: in hex, could use up to 10 possible characters as pipes. i.e. 4 
bits. Maybe this is fine. Maybe use four bits for each in/out? That seems
plausible.

  0
1   3
  2
  
So

-o
 |
 
would be 0110

and

 |
-o-

would be 1101

So we would never use 0000.

Since the level is 80 x 24 in size, this means that each file is 40 x 24 
bytes i.e. 960 bytes.

Note that we will assume that the boundary is drawn already. Because curses 
is good at that.
"""
LEVEL_WIDTH = 80
LEVEL_HEIGHT = 24
import curses

class LvlFile(object):
    def __init__(self, n):
        """
        Loads the file for level n
        """
        self.tiles = [[0 for i in range(LEVEL_WIDTH)] for j in range(LEVEL_HEIGHT)]
        
        f = open("levels/%d.dat" % n)
        contents = f.readlines()
        f.close()
        
        # Read it into the double array
        for j in range(LEVEL_HEIGHT):
            for i in range(LEVEL_WIDTH / 2):
                self.tiles[j][2 * i]     = ord(contents[j][i]) / 16
                self.tiles[j][2 * i + 1] = ord(contents[j][i]) % 16
#                if self.tiles[j][2 * i] > 0:
#                    raise Exception("Even: %d" % self.tiles[j][2 * i])
#                if self.tiles[j][2 * i + 1] > 0:
#                    raise Exception("Odd: %d" % self.tiles[j][2 * i + 1])
                    
    
    def getTile(self, x, y):
        """
        Returns the curses code for the tile at position (x, y).
        """
        #return self.tiles[y][x] > 0
        t = self.tiles[y][x]
        if t == 0:
            return 0
        if t == 0x5: # 0101
            return curses.ACS_VLINE
        if t == 0xa: # 1010
            return curses.ACS_HLINE
        if t == 0x3: # 0011
            return curses.ACS_LRCORNER
        if t == 0x6: # 0110
            return curses.ACS_URCORNER
        if t == 0xc: # 1100
            return curses.ACS_ULCORNER
        if t == 0x9: # 1001
            return curses.ACS_LLCORNER
        if t == 0x7: # 0111
            return curses.ACS_RTEE
        if t == 0xE: # 1110
            return curses.ACS_TTEE
        if t == 0xD: # 1101
            return curses.ACS_LTEE
        if t == 0xB: # 1011
            return curses.ACS_BTEE
        if t == 0xf: # 1111
            return curses.ACS_PLUS
        
