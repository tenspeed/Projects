# This is the Database class. The Database class handles any task relating to the movie database including,
# opening the file where the movie information is stored, searching for movies based on search criteria,
# and adding new movies to the database.
class Database(object):

	def __init__(self):

		# Initialize the movie database by calling the load_db() method.
		self.load_db()

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

	# The add_movies() method accepts a list of new movie information to add to the
	# database.
	def add_movies(self, new_movie_list):

		# Open the bmdb.txt file where the movie information is stored and then
		# append each new piece of info to the file.
		with open("bmdb.txt", 'a') as self.f:
			for i in range(len(new_movie_list)):
				entry = new_movie_list.pop(0)
				self.f.write(entry)

		# Call the load_db() method to re-initialize the database after the new
		# information has been added.
		self.load_db()

	# The load_db() method initializes the database. It's called when the database object
	# is first created and whenever new movie info is added by the user.
	def load_db(self):

		# Open the text file where the movie information is saved and read it into the variable 'data'
		# as a string.
		with open("bmdb.txt", 'a+') as f:
			data = f.read()

		# Remove the last ';' from the end of the string.
		data = data[:-1]

		# The five categories of information in the text file are 'Title', 'Genre', 'Director',
		# 'Year', and 'Actors', in that order. Each entry in the text file is separated by a
		# semi-colon. Here, we take the raw information from the 'data' string and create a list
		# containing the information for each category by looking for the semi-colons.
		movies = data.split(';')

		# Create a variable 'n' which will tell us how many movies are in the list.
		self.n = len(movies) / 5

		# Here we create a 2D list which will hold all of our movie data. A 2D list
		# provides us with an intuitive organizational structure for searching and
		# adding movies to the database.
		self.moviedb = [[[None] for i in range(5)] for i in range(self.n)]
		for i in range(self.n):
			for j in range(5):
				word = movies.pop(0)
				self.moviedb[i][j] = word

#-----------------------------------------------------------------------------------------------------------

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

		3) View entire collection

		4) Quit program

		"""
		print "\n" * 5
		answer = raw_input("> ")

		if answer == '1':
			# Check to see if there are any movies in the database; if not, tell
			# the user to add some.
			if self.my_movies.n == 0:
				print "\n" * 50
				print "The database is empty! Try adding some movies!"
				raw_input("\nPress enter to return to main menu.")
				print "\n" * 50
				return False
			else:
				self.search_prompt()
		elif answer == '2':
			self.get_input()
		elif answer == '3':
			# Check to see if there are any movies in the database; if not, tell
			# the user to add some.
			if self.my_movies.n == 0:
				print "\n" * 50
				print "The database is empty! Try adding some movies!"
				raw_input("\nPress enter to return to main menu.")
				print "\n" * 50
				return False
			else:
				self.view_collection()
		elif answer == '4':
			print "\n" * 50
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
	
	# The view_collection() method sorts the movie database by Title
	# and displays it to the screen. 
	def view_collection(self):

		print "\n" * 50
		print """
Title, Genre, Director(s), Year
-------------------------------
		"""
		self.my_movies.moviedb.sort()
		for i in range(self.my_movies.n):
			print "%s, %s, %s, %s\n" % (self.my_movies.moviedb[i][0], self.my_movies.moviedb[i][1],
										self.my_movies.moviedb[i][2], self.my_movies.moviedb[i][3])

		raw_input("\nPress enter to return to main menu.")
		print "\n" * 50

	# The get_input() method displays prompts on the screen for the user
	# to enter new movie information to the database. get_input() properly
	# formats the new information, puts it in a list, and then calls the database
	# object's add_movies() method to add the new information to the database.
	def get_input(self):

		catagories = ['Title', 'Genre', 'Director', 'Year', 'Actors']
		new_movies = []
		print "*** Type 'quit()' to return to main menu. ***"
		print "*** Type 'stop()' when done entering movies. ***"
		print "*** Incomplete entries will not be saved!!! ***\n\n"

		# Collect new movie input until the user types 'quit()' or 'stop()'
		# 'quit()' returns to the main menu without saving any input, while
		# 'stop()' ends the data entry, checks for incomplete movie input and
		# removes them, and then updates the database.
		while True:
			for i in range(5):
				entry = raw_input("Enter the %s: " % catagories[i]) + ';'
				if entry == "quit();":
					return
				elif entry == "stop();":
					# Check if the user stopped with an incomplete movie entry.
					# If so, delete the incomplete items before updating the database.
					if len(new_movies) % 5 != 0:
						# Calculate how many items need to be removed from the list.
						num_extra = len(new_movies) - ((len(new_movies) / 5) * 5)
						# Iterate until all the incomplete items have been removed.
						for j in range(num_extra):
							new_movies.pop(-1)
					else:
						pass
					# Update the database with the new movies.
					self.my_movies.add_movies(new_movies)
					raw_input("\nPress enter to return to main menu.")
					print "\n" * 50
					return
				else:
					new_movies.append(entry)
		
#-----------------------------------------------------------------------------------------------------------

print "\n" * 50
print """
			*** Welcome to Bob's Movie Database ***
		"""
# Condition for quitting the program.
quit = False

movies = Database()
prompts = GUI(movies)

# Main program loop.
while not quit:
	quit = prompts.main_menu()