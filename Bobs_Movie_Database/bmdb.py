class Database(object):
	
	def __init__(self):
		self.f = None
		with open("bmdb.txt") as self.f:
			self.data = self.f.read()
		self.movies = self.data.split('; ')
		self.n = len(self.movies) / 4
		self.moviedb = [[[None] for i in range(4)] for i in range(self.n)]
		for i in range(self.n):
			for j in range(4):
				self.word = self.movies.pop(0)
				self.moviedb[i][j] = self.word

class GUI(object):
	pass

class Prompt(GUI):
	pass

my_movies = Database()
user_input = Prompt()