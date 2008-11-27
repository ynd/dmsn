import os
import traceback

class Commands:
	def __init__(self,DMsn):
	 self.dMsn = DMsn	
	 self.__CommandMapMethod = {}
         for each in self.__findAllCommands():
	  self.add(each)

	def __findAllCommands(self):
	 "Find commands in the path commands/"

	 CommandList = os.listdir("commands/")
	 CommandList = [ file[0:-3] for file in CommandList
	  if file[-3:] == ".py" and file != "__init__.py" ]
         
	 return CommandList


        def get_commandList(self):
 	 return self.__CommandMapMethod

        def __loadCommand(self, command):
	  try:
	   module = __import__("commands." + command)
	   module_command = getattr(module,command)
	   method = getattr(module_command, command)
	   self.__CommandMapMethod[command] = [module_command,1]
	   return 1

	  except:
	   return 0


	def add(self, command):
	 """
	 Load a new command, or reload an old one who has been deleted.
	 @ returns:
	  1 if success
	  -1 if command already exist
	  0 error while loading the command
	 """

         exist = self.__CommandMapMethod.keys().count(command)
	 if exist == 0:
	  return self.__loadCommand(command) 
         
         info = self.__CommandMapMethod[command]
         # command is already added
         if info[1] == 1:
	  return -1
         
         # this command needs to be reloaded since it was "deleted"
	 module = info[0]
	 try:
          reload(module)
	  info[1] = 1
	  return 1
         except:
          return 0

	def rem(self, command):
	 """
	 This is a little hack :/ We kind of remove the command by 
	 writing 0 in the list of command. When the user wants to 
	 add it, we'll use reload() instead of import().. It seems that
	 Python doesn't like the import, del, import.. he preferes 
	 import and reload().. so this is a nasty hack that can 
	 sometime work :`/
	 """
	 exist = self.__CommandMapMethod.keys().count(command)
	 if exist == 0:
	  return 0
         
         if self.__CommandMapMethod[command][1] == 0:
	  return 0

         self.__CommandMapMethod[command][1] = 0
	 return 1

	def reload(self, command):
		result = self.rem(command)
		if result != 1:
		 return result

		result = self.add(command)
		return result
	
	
	def parse(self, cmds):
         # removing /
	 if cmds[0][0] == '/':
	  command = cmds[0][1:] 
	 else:
	  command = cmds[0]
	 
	 if self.__CommandMapMethod.keys().count(command) == 0:
	  return -1
	 
         commandInfo = self.__CommandMapMethod[command]
	 if commandInfo[1] == 0:
	  return -1
      
         try:
          method = getattr(commandInfo[0], command)	   
	  method(self.dMsn, cmds[1:])
	  return 1

         except:
 	  self.dMsn.T.error("Exception occured")
	  exc = traceback.format_exc()
	  self.dMsn.Terminal.writeline(exc)
	  return 0
