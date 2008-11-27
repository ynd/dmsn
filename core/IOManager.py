import select
import sys

class IOManager:
 def __init__(self, DMsn):  
  self.dMsn = DMsn
 
 def pool(self):
  pool = select.select([sys.stdin.fileno()], [], [], 0)

  input = pool[0]
 
  if len(input) > 0:
   data = self.dMsn.Terminal.readline()
   if data[0] == 1:
    self.parse(data[1])

  self.dMsn.TM.check() 


 def parse(self, line):
  cmds = line.split()

  if len(cmds) == 0 or (len(cmds[0]) == 1 and cmds[0][0] == '/'):
   self.dMsn.T.error('error while parsing command')
   return

  if cmds[0][0] == '/':
   error = self.dMsn.CM.parse(cmds)
   if error == -1:
	   self.dMsn.T.error('\'' + cmds[0][1:] + '\'' + ' no such command')
  else:
   self.dMsn.WindowsManager.parse(cmds)

 
