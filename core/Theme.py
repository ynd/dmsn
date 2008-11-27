import sys
import curses

class Theme:
 def __init__(self, DMsn):
  self.dMsn = DMsn;
  self.list_colors = [curses.COLOR_WHITE, curses.COLOR_GREEN, curses.COLOR_RED]

 def error(self, msg):
  text  = " [!] " + msg 
  self.dMsn.Terminal.writeline(text, color=3)

 def success(self, msg):
  text = " [@] " + msg
  self.dMsn.Terminal.writeline(text, color=2)

 def info(self, msg):
  text = " - " + msg
  self.dMsn.Terminal.writeline(text, color=1)

 def prompt(self):
  w = self.dMsn.WindowsManager.currentWindow
  return '(' + w + ") >>  " 



