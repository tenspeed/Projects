# bmdb.py version 1.1
# Written by Todd Smith
# 10/2/2013
# Licence:
#		This file is released under the Lesser GNU Public License.
#
#-----------------------------------------------------------------------------------------------------------

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
			for j in range(6):
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

		# The six categories of information in the text file are 'Title', 'Genre', 'Director',
		# 'Year', 'DVD/Bluray', and 'Actors', in that order. Each entry in the text file is separated by a
		# semi-colon. Here, we take the raw information from the 'data' string and create a list
		# containing the information for each category by looking for the semi-colons.
		movies = data.split(';')

		# Create a variable 'n' which will tell us how many movies are in the list.
		self.n = len(movies) / 6

		# Here we create a 2D list which will hold all of our movie data. A 2D list
		# provides us with an intuitive organizational structure for searching and
		# adding movies to the database.
		self.moviedb = [[[None] for i in range(6)] for i in range(self.n)]
		for i in range(self.n):
			for j in range(6):
				word = movies.pop(0)
				self.moviedb[i][j] = word
		# Sort the database by alphabetical order.
		self.moviedb.sort()

#-----------------------------------------------------------------------------------------------------------

# This is the GUI class. The GUI class handles most of the display to the terminal and feeds user input to a
# database object for searching and adding new titles to the movie database.
class GUI(object):

	def __init__(self, db_object):

		self.my_movies = db_object
	
	def main_menu(self):

		dummy_list = []

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
			print "\n" * 50
			self.get_input(dummy_list)
			print "\n" * 50
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

		while True:
			print "\n" * 50
			print "*** Type quit() at any time to return to the main menu. ***\n\n\n"
			print "Enter search term:"
			answer = raw_input("> ").lower()
			print "\n" * 50
			if answer == 'quit()':
				print "\n" * 50
				return
			else:
				pass
			search_results = self.my_movies.search(answer)
			print "Found %d matches:" % len(search_results)
			print "------------------\n"
			for element in search_results:
				# This fancy line takes each element in search_results and capitalizes every
				# word. I could have used element.title() but that method doesn't handle
				# apostrophes gracefully.
				element = " ".join(word[0].upper() + word[1:] for word in element.split())
				print element + "\n"
			answer = raw_input("\nPress enter to search again.").lower()
			if answer == 'quit()':
				print "\n" * 50
				return
			else:
				pass
	
	# The view_collection() method sorts the movie database by Title
	# and displays it to the screen. 
	def view_collection(self):

		print "\n" * 50
		print """
Title, Genre, Director(s), Year
-------------------------------
		"""
		temp_list = []
		for i in range(self.my_movies.n):
			# Fill the temporary list with one set of movie data.
			for j in range(5):
				temp_list.append(self.my_movies.moviedb[i][j])
			# Capitolize every word for each piece of movie data in temp_list.
			for k in range(5):
				element = temp_list[k]
				element = " ".join(word[0].upper() + word[1:] for word in element.split())
				temp_list[k] = element
			# If the movie is a DVD, make sure 'DVD' is printed and not 'Dvd'
			if temp_list[4] == 'Dvd':
				temp_list[4] = 'DVD'
			else:
				pass
			print "%s, %s, %s, %s, %s\n" % (temp_list[0], temp_list[1], temp_list[2],
											temp_list[3], temp_list[4])
			# Delete the contents of temp_list for the next iteration.
			del temp_list[:]

		raw_input("\nPress enter to return to main menu.")
		print "\n" * 50

	# The get_input() method displays prompts on the screen for the user
	# to enter new movie information to the database. get_input() properly
	# formats the new information, puts it in a list, and then calls the database
	# object's add_movies() method to add the new information to the database.
	def get_input(self, a_list):

		catagories = ['Title', 'Genre', 'Director', 'Year', 'Format', 'Actors']
		new_movies = a_list
		print "*** Type done() when finished entering movies. ***\n"
		print "*** Type quit() at any time to return to main menu. ***\n"
		print "*** Incomplete entries will not be saved!!! ***\n\n\n"

		# Collect new movie input until the user types 'quit()' or 'done()'
		# 'quit()' returns to the main menu without saving any input, while
		# 'done()' ends the data entry, checks for incomplete movie input and
		# removes them, and then updates the database.
		while True:
			for i in range(6):
				entry = raw_input("Enter the %s: " % catagories[i]).lower()
				if entry == 'quit()':
					print "\n" * 50
					return
				elif entry == 'done()':
					# Check if the user stopped with an incomplete movie entry.
					# If so, delete the incomplete items before updating the database.
					if len(new_movies) % 6 != 0:
						# Calculate how many items need to be removed from the list.
						num_extra = len(new_movies) - ((len(new_movies) / 6) * 6)
						# Iterate until all the incomplete items have been removed.
						for j in range(num_extra):
							new_movies.pop(-1)
					else:
						pass
					# Update the database with the new movies.
					self.my_movies.add_movies(new_movies)
					print "\nMovie database updated!"
					raw_input("\nPress enter to return to main menu.")
					print "\n" * 50
					return
				else:
					# Check to make sure that duplicate titles aren't being entered.
					if i == 0:
						duplicate = self.my_movies.search(entry)
						# If a duplicate has been entered, call get_input() recursively,
						# pass in the current new_movies list, and continue where you
						# left off.
						if (len(duplicate) != 0) or ((entry + ";") in new_movies):
							print "\n" * 50
							print "This movie is already in the database!\n\n\n"
							self.get_input(new_movies)
							return
						else:
							pass
					entry += ";"
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