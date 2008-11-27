from time import *

class TimerManager:
 def __init__(self, dMsn):
  self.dMsn = dMsn
  self.last_time = time()
  self.last_second = -1

 def check(self):
  diff = time() - self.last_time

  if diff >= 1 and self.last_second == 0:
   self.call_second()
   self.last_second = time()

  if (time() - self.last_second) > 1:
   self.last_second = 0


 def call_second(self):
  str_time = str('[' + str(ctime()) + ']')
  self.dMsn.Terminal.print_statusbar(str_time)
