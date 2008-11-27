import getopt

def usage(dMsn):
 dMsn.T.error('Usage [(-a | --add) <window name>, (-r | --remove) <window name>, (-s | --switch) <window name>, (-d | --default) <name> | (-l | --list), (-h | --help)]')

def add(dMsn, name):
 result = dMsn.WindowsManager.add(name)

 if result[0] <= 0:
  dMsn.T.error(result[1])
 else:
  dMsn.T.success('Window ' + name + ' succesfully created.')

def remove(dMsn, name):
 result = dMsn.WindowsManager.rem(name)

 if (result <= 0):
  dMsn.T.error(result[1])
 else:
  dMsn.T.success('Window ' + name + ' succesfully removed.');

def switch(dMsn, name):
 dMsn.WindowsManager.switch(name)

def list(dMsn):
 li = dMsn.WindowsManager.windowsList
 printable = [w.name for w in li]

 dMsn.T.info(str(printable))

def default(dMsn, name):
 dMsn.WindowsManager.default_add(name)

def window(dMsn, args):
 if (len(args) == 0):
  usage(dMsn)
  return

 try:
	 (optlist, realargs) = getopt.getopt(args, 'a:r:s:lhd:', ['add=', 'remove=', 'switch=', 'help', 'list', 'default='])

 except getopt.GetoptError, err:
  dMsn.T.error(str(err))
  usage(dMsn)
  return

 for o, a in optlist:
  if o in ('-h','--help'):
   usage(dMsn)
   return
  elif o in ('-a','--add'):
   add(dMsn, a)
   return
  elif o in ('-r','--remove'):
   remove(dMsn, a)
   return
  elif o in ('-l','--list'):
   list(dMsn)
   return
  elif o in ('-d', '--default'):
   default(dMsn, a)
   return
  elif o in ('-s','--switch'):
   switch(dMsn, a)
   return

 usage(dMsn)
