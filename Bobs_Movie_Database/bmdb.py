from sys import exit

class Database(object):
	
	def __init__(self):
		self.f = None
		with open("bmdb.txt") as self.f:
			self.data = self.f.read()
		self.movies = self.data.split('; ')
		self.n = len(self.movies) / 5
		self.moviedb = [[[None] for i in range(5)] for i in range(self.n)]
		for i in range(self.n):
			for j in range(5):
				self.word = self.movies.pop(0)
				self.moviedb[i][j] = self.word
		print self.moviedb

		print """
			*** Welcome to Bob's Movie Database ***
		"""

	def search(self, query):

		for i in range(self.n):
			for j in range(5):
				if query in self.moviedb[i][j]:
					print self.moviedb[i][:]
				else:
					pass

class GUI(object):
	pass

class Prompt(GUI):

	def __init__(self, db_object):

		self.my_movies = db_object
	
	def main_menu(self):

		print """
				***   Main Menu   ***

		Please select from the following:

		1) Search by Title, Actors, Genre, Director, or Year

		2) Add a new movie

		Press CTRL-C to exit

		"""

		answer = raw_input("> ")

		if answer == "1":
			self.search_prompt()
		elif answer == "2":
			self.add_movie_prompt()
		else:
			print "Not a valid choice."

	def search_prompt(self):

		print """
		Enter search term:
		"""
		answer = raw_input("> ")
		my_movies.search(answer)


	def add_movie_prompt(self):
		print "adding movie"

my_movies = Database()
user_input = Prompt(my_movies)

while True:
	user_input.main_menu()