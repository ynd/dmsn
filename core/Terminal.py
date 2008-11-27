import curses
import string
import time

class Terminal:
 def __init__(self, DMsn):
  self.buffer = "" 
  self.dMsn = DMsn
  self.history = []
  self.cursor_history = 0
  self.screen = ''
  self.position_buffer = 0
  self.relative_position = 0
  self.position_screen = 0
  self.dontscroll = 0

 def load(self):
  try:
   self.screen = curses.initscr()
   curses.start_color()
   curses.noecho()
   curses.cbreak()
   self.screen.keypad(1)
   curses.use_default_colors()
   
   i = 1

   for x in self.dMsn.T.list_colors:
    curses.init_pair(i, x, -1)
    i += 1


   self.screen.scrollok(1)
   self.screen.setscrreg(0, curses.LINES - 3)
   self.newline()
  
     

  except:
   print 'Impossible to initialize curses..'   
   exit(1)

 def unload(self):
  self.screen.keypad(0)
  curses.echo()
  curses.nocbreak()
  curses.endwin()



 def readline(self):
  alt = 0

  while 1:
   i = self.screen.getch()
   c=''
   
   if alt == 1:
    alt=0
    self.alt(i)
    continue

   elif i == curses.KEY_DOWN:
    self.down()
    continue;
   elif i == curses.KEY_UP:
    self.up()
    continue
   elif i == curses.KEY_LEFT:
    self.left()
    continue
   elif i == curses.KEY_RIGHT:
    self.right()
   elif i in (curses.KEY_BACKSPACE,127):
    self.backspace()
    continue
   elif i in (curses.KEY_ENTER, 10):
    text = self.newline()
    return (1, text)
   elif i == 27:
    alt=1
    continue
   elif self.is_normal_caracter(i):
    c = chr(i)   
    self.normal_char(c)
   else: 
    pass
 
 def is_normal_caracter(self, i):
  try:
   c = chr(i)
   if c.isalnum: return 1
   elif c == ' ': return 1

  except:
   return 0
  return 0
 
 def newline(self):
  text = self.buffer

  self.buffer = ''

  self.clearline()
  self.print_prompt()

  self.history.insert(1, text)
  self.cursor_history = 0

  self.position_buffer = 0
  self.relative_position = 0

  return text


 def left(self):
  """
  Move the buffer's cursor to the left.
  """
  self.relative_position -= 1
  if self.relative_position < 0:
   self.relative_position = 0

  self.position_buffer -= 1
  if self.position_buffer < 0:
   self.position_buffer = 0

  self.wrap_prompt()


 def right(self):
  """
  Move the buffer's cursor to the right.
  """
  disponible_space = curses.COLS - len(self.dMsn.T.prompt()) - 1

  if self.relative_position < disponible_space and self.relative_position < len(self.buffer):
   self.relative_position += 1


  if self.position_buffer < len(self.buffer):
   self.position_buffer += 1

  self.wrap_prompt()

 def down(self):
  if self.cursor_history <= 0:
   return

  self.cursor_history -= 1
  self.clearline()
  self.buffer = self.history[self.cursor_history]
  self.print_prompt()
  self.ajust_cursor()
  self.wrap_prompt()


 def up(self):
  if self.cursor_history >= len(self.history)-1:
   return

  self.cursor_history += 1
  self.clearline()
  self.buffer = self.history[self.cursor_history]
  self.ajust_cursor()
  self.wrap_prompt()

 def ajust_cursor(self):
  disponible_space = curses.COLS - len(self.dMsn.T.prompt()) - 1
  self.position_buffer = len(self.buffer)
  self.relative_position = len(self.buffer)
  if self.relative_position > disponible_space:
   self.relative_position = disponible_space

 

	
 def backspace(self):
  """
  delete before-cursor caracter
  """
  if self.position_buffer == 0:
   return
  
  self.buffer = self.buffer[0:self.position_buffer - 1] + self.buffer[self.position_buffer:]
  self.left()
  self.wrap_prompt()


  

 def normal_char(self, c):
  self.buffer = self.buffer[0:self.position_buffer] + c + self.buffer[self.position_buffer:]
  
  self.position_buffer += 1
  self.relative_position += 1
  
  disponible_space = curses.COLS - len(self.dMsn.T.prompt()) - 1

  if self.relative_position > disponible_space:
   self.relative_position = disponible_space

  self.wrap_prompt()


 def alt(self, i):
  try:
   self.writeline(str(i))
   c = chr(i)
   n = string.atoi(c) 
   self.dMsn.WindowsManager.switch_n(n)
  except:
   pass

 def wrap_prompt(self):
  """
  make a scroll effect if we write pass the length of the 
  window
  """

  prompt = self.dMsn.T.prompt()
  prompt_size = len(prompt)

  where_y = curses.LINES-1
   
  begin_buffer = self.position_buffer - self.relative_position 
  disponible_space = curses.COLS - prompt_size - 1

  self.clearline()
  self.screen.addstr(where_y, 0, prompt + self.buffer[begin_buffer:begin_buffer + disponible_space], curses.color_pair(0)) 
  self.screen.move(where_y, prompt_size + self.relative_position)
  self.screen.refresh()

 def print_prompt(self):
  p = self.dMsn.T.prompt()
  where_y = curses.LINES-1
  where_x = len(p)

  self.screen.move(where_y, where_x)
  self.screen.addstr(where_y, 0, p, curses.color_pair(1))
  self.screen.refresh()

 def print_statusbar(self, text):
  # we need to clear it.
  self.screen.move(curses.LINES-2, 0)
  self.screen.clrtoeol()

  self.screen.addstr(curses.LINES-2, 0, text, curses.color_pair(2))
  self.wrap_prompt()

 def clearline(self):
  self.screen.move(curses.LINES - 1, 0)
  self.screen.clrtoeol()

 def writeline(self, text, save_line=1, wrap=1, color=0):
  if save_line:
   self.dMsn.WindowsManager.line_added(text, color)

  lines = self.wrapline(text, curses.COLS-1)

  for line in lines:
   self._write_single_line(line, color)

  if wrap==1:
   self.wrap_prompt()

 def _write_single_line(self, line, color):
   if self.position_screen > curses.LINES-3:
    self.screen.scroll(1)
    self.position_screen = curses.LINES-3

   self.screen.move(self.position_screen, 0)
   self.screen.addstr(line, curses.color_pair(color))

   self.position_screen += 1
  

 def clearscreen(self, notify=1):
  self.screen.scroll(curses.LINES)
  self.screen.refresh()
  self.position_screen = 0
  if notify:
   self.dMsn.WindowsManager.screen_cleared()

 def wrapline(self, line, line_size):
  list_line = []
  current_line = ''

  words = line.split(' ')

  for word in words:
   # 1. The word is larger than the max width.
   #    We need to trunc it.
   while len(word) >= line_size:
    if current_line == '':
     current_line = word[:line_size]
     word = word[line_size:]
    else:
     word_width = line_size - len(current_line) - 1
     current_line += ' ' + word[:word_width]
     word = word[word_width:]
    
    list_line.append(current_line)
    current_line = ''

   if len(word) + len(current_line) >= line_size:
    list_line.append(current_line)
    current_line = ''

   if word != '':
    if current_line == '':
     current_line = word
    else:
     current_line += ' ' + word


   
  if current_line != '':
   list_line.append(current_line)

  return list_line

    

    

 

  
 
 


