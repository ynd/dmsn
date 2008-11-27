def help(dMsn, args):
 dMsn.T.success('Here is the list of commands you can use:')

 cmds = dMsn.CM.get_commandList() 
 list = [x for x in cmds.keys()
	 if cmds[x][1] == 1]
 

 dMsn.T.success(str(list))
 dMsn.T.info('')

 return 1

