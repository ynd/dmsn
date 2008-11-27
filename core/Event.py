class Event:
	def __init__(self):
		self.__observers = []
	
	def add(self, method_name):
		self.__observers.append(method_name)
	
	def notify(self, args):
		for method_name in self.__observers:
			method_name(args);

	def rem(self, method_name):
		try:
		 self.__observers.remove(method_name)
		except:
		 pass
			
