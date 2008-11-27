import curses
import sys
import traceback
class gb:
 scr = ''
 buffer = ''

def bleh():
 gb.scr = curses.initscr()

 gb.scr.move(curses.LINES-1,0)
 while 1:

  i = gb.scr.getch()
  c = chr(i)

  gb.buffer += c

  if len(gb.buffer) < curses.COLS:
   gb.scr.addstr(curses.LINES-1,0,gb.buffer)
  else:
   gb.scr.addstr(curses.LINES-1,0,gb.buffer[len(gb.buffer) - curses.COLS + 1:])




def restore():
 curses.echo()
 curses.nocbreak()
 curses.endwin()

try:
 bleh()
 restore()

except:
 restore()
 traceback.print_exc()
 
