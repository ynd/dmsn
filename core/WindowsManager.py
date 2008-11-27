from Window import *
import time

class WindowsManager:
 def __init__(self, DMsn):
  self.dMsn = DMsn
  self.windowsList = []

  status = Window('status')
  self.windowsList.append(status)
  
  self.currentWindow = 'status'

 def add(self, name):
  if len(name) < 2:
   return (-1, 'Name is too short.')

  if name in [n.name for n in self.windowsList]:
   return (0, name + ' already exist')

  window = Window(name)
  self.windowsList.append(window)
  return (1, 'success')
 
 def rem(self, name):
  if name not in [n.name for n in self.windowsList]:
   return (0, 'this window doesn\'t exist.')
  
  if name == "status":
   return (-1, 'Impossible to close %status.')

  for window in self.windowsList:
   if window.name == name:
    self.windowsList.remove(window)
    break;
  
  if self.currentWindow == name:
   self.switch('status')
 
  return (1, 'success')

 def switch(self, name):
  if name not in [n.name for n in self.windowsList]:
   return (-1, 'this window doesn\'t exist.')

  self.currentWindow = name
  self.print_lines()

  return (1, 'success')
 
 def default_add(self, name):
  self.get_currentWindow().default_chat.append(name)

 def switch_n(self, n):
  if n < 0 or n > len(self.windowsList):
   return
 
  self.switch(self.windowsList[n-1].name)
   
 def get_currentWindow(self):
  for window in self.windowsList:
   if window.name == self.currentWindow:
    return window

  return None
 
 def parse(self, text):
  default = self.get_currentWindow().default_chat

  if default:
   self.dMsn.T.info('sent: ' + ' '.join(text) + ' to: ' + str(default))
  else:
   self.dMsn.T.error('Talking to nowhere dummy')

 def line_added(self, line, color):
  w = self.get_currentWindow()
  if not w: return
  w.add_line(line,color)

 def print_lines(self):
  w = self.get_currentWindow()
  if not w: return

  self.dMsn.Terminal.clearscreen(notify=0)
  for each in w.lines:
   if each[2] == 1:
    self.dMsn.Terminal.writeline(each[0], 0, 0, color=each[1])

  self.dMsn.Terminal.wrap_line()


 def screen_cleared(self):
  for line in self.get_currentWindow().lines:
   line[2] = 0
