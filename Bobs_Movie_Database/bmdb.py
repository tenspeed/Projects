# This is the Database class. The Database class handles any task relating to the movie database including,
# opening the file where the movie information is stored, searching for movies based on search criteria,
# and adding new movies to the database.
class Database(object):
	
	def __init__(self):

		self.f = None

		# Open the text file where the movie information is saved and read it into the variable 'data'
		# as a string.
		with open("bmdb.txt") as self.f:
			self.data = self.f.read()

		# The five categories of information in the text file are 'Title', 'Genre', 'Director',
		# 'Year', and 'Actors', in that order. Each entry in the text file is separated by a
		# semi-colon. Here, we take the raw information from the 'data' string and create a list
		# containing the information for each category by looking for the semi-colons.
		self.movies = self.data.split('; ')

		# Create a variable 'n' which will tell us how many movies are in the list.
		self.n = len(self.movies) / 5

		# Here we create a 2D list which will hold all of our movie data. A 2D list
		# provides us with an intuitive organizational structure for searching and
		# adding movies to the database.
		self.moviedb = [[[None] for i in range(5)] for i in range(self.n)]
		for i in range(self.n):
			for j in range(5):
				self.word = self.movies.pop(0)
				self.moviedb[i][j] = self.word
		print "\n" * 50
		print """
			*** Welcome to Bob's Movie Database ***
		"""

	# The search() method accepts a query in the form of a string as an argument and
	# searches through the movie database looking for other strings that match or are
	# a partial match to the query.
	def search(self, query):

		results = []

		for i in range(self.n):
			for j in range(5):
				if query in self.moviedb[i][j]:
					results.append(self.moviedb[i][0])
				else:
					pass
		return results

	# The add_movie() method has not been implemented yet.
	def add_movies(self, new_movie_list):
		pass

# This is the GUI class. The GUI class handles most of the display to the terminal and feeds user input to a
# database object for searching and adding new titles to the movie database.
class GUI(object):

	def __init__(self, db_object):

		self.my_movies = db_object
	
	def main_menu(self):

		print """
				***   Main Menu   ***

		Please select from the following:

		1) Search by Title, Actors, Genre, Director, or Year

		2) Add a new movie

		3) Quit program

		"""
		answer = raw_input("> ")

		if answer == "1":
			self.search_prompt()
		elif answer == "2":
			self.add_movie_prompt()
		elif answer == '3':
			return True
		else:
			raw_input("Not a valid choice. Press enter.")
			print "\n" * 50

	# The search_prompt() method is called if the user selects the search option
	# from the main menu. search_prompt() asks the user for a search term and
	# calls the database object's search() method to look for matches.
	def search_prompt(self):

		print "\n" * 50
		print "Enter search term:"
		
		answer = raw_input("> ")
		print "\n" * 50
		search_results = self.my_movies.search(answer)
		print "Found %d matches:\n" % len(search_results)
		for element in search_results:
			print element

		raw_input("\nPress enter to return to main menu.")
		print "\n" * 50

	# The add_movie_prompt() method has not been implemented yet.
	def add_movie_prompt(self):
		
		catagories = ['Title', 'Genre', 'Director', 'Year', 'Actors']
		new_movies = []

		for i in range(5):
			entry = raw_input("Enter the %s: " % catagories[i])
			new_movies.append(entry)

		self.my_movies.add_movies(new_movies)

# Condition for quitting the program.
quit = False

movies = Database()
prompts = GUI(movies)

# Main program loop.
while not quit:
	quit = prompts.main_menu()