class Window:
 def __init__(self, name):
  self.name = name
  self.default_chat = []
  self.lines = []

 def add_line(self, line, color):
  self.lines.append([line,color,1])
	
