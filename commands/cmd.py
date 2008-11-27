import getopt

def usage(dMsn):
 dMsn.T.error('Usage [(-a | --add) <command name>, (-r | --remove) <command name>, (-u | --update) <command name>, (-l | --list), (-h | --help)]')

def add(dMsn, command):
 result = dMsn.CM.add(command)

 if result == 1:
  dMsn.T.success(command + " succesfully added.")

 elif result == 0:
  dMsn.T.error('Failed to add ' + command)
 
 elif result == -1:
  dMsn.T.error(command + " already exist. Maybe you are looking for the --update option?")

def remove(dMsn, command):
 result = dMsn.CM.rem(command)

 if (result == 1):
  dMsn.T.success(command + " succesfully removed.")
 elif result == 0:
  dMsn.T.error('Failed to remove ' + command);

def update(dMsn, command):
 result = dMsn.CM.reload(command)

 if result==1:
  dMsn.T.success(command + ' sucessfully updated')
 elif result == 0:
  dMsn.T.error('Failed to update ' + command)
 elif result == -1:
  dMsn.T.error(command + ' isn''t loaded. You need to use the "cmd -a <command>" option.')


def list(dMsn):
 li = dMsn.CM.get_commandList()
 commands = [x for x in li.keys()
		 if li[x][1] == 1]

 dMsn.T.info(str(commands))

def cmd(dMsn, args):
 if (len(args) == 0):
  usage(dMsn)
  return

 try:
  (optlist, realargs) = getopt.getopt(args, 'a:r:u:lh', ['add=', 'remove=', 'update=', 'help', 'list'])

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
  elif o in ('-u','--update'):
   update(dMsn, a)
   return

 usage(dMsn)
