class Database(object):

	def __init__(self):
		self.f = None
		with open("bmd.txt") as f:
			self.movies = f.read()

class GUI(object):
	pass

class Prompt(GUI):
	pass

my_movies = Database()
user_input = Prompt()

print my_movies.movies