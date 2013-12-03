# bmdb.py version 3.0
# Written by Todd Smith
# 10/15/2013
# Licence:
#		This file is released under the Lesser GNU Public License.
#
#-----------------------------------------------------------------------------------------------------------
# This is the Database class. The Database class handles any task relating to the movie database including,
# opening the file where the movie information is stored, searching for movies based on search criteria,
# and adding new movies to the database.
from sqlalchemy import *

class Database(object):

	# Upon instantiation, a permanent database property is created by calling the load_db() method.
	def __init__(self):
		pass
	# The search() method accepts a query in the form of a string as an argument and
	# searches through the movie database looking for other strings that match or are
	# a partial match to the query. If a match is found, search() returns a formated,
	# 2D list of all the matching movie information.
	def search(self, query):

		temp_list = []
		query = query.lower()
		for i in range(len(self.the_database)):
			for j in range(6):
				if query in self.the_database[i][j]:
					for k in range(6):
						temp_list.append(self.the_database[i][k])
					break
				else:
					pass
		results = self.list_builder(temp_list, 6)
		results = self.list_formatter(results)
		return results

	# The add_new() method accepts a dictionary of new movie information to add to the
	# database. add_new() check for duplicates and then if none are found, writes the new
	# movie information to bmdb.txt and reinitializes the_database.
	def add_new(self, new_movie_dict):

		keys = ['title', 'genre', 'director', 'year', 'format', 'actors']
		# Open the bmdb.txt file where the movie information is stored and then
		# append each new piece of info to the file.
		with open("bmdb.txt", "a") as f:
			for i in range(6):
				new_entry = (new_movie_dict.get(keys[i])).lower()
				print new_entry
				# Since all titles should be unique, if the new title matches any existing
				# titles in the_database, then the new movie entry is a duplicate and can
				# be thrown out.
				if i == 0:
					duplicate = self.search(new_entry)
					if len(duplicate) != 0:
						f.close()
						return
				if len(new_entry) == 0:
					new_entry = "n/a"
				new_entry += ";"
				f.write(new_entry)

		# Call the load_db() method to re-initialize the_database after the new
		# information has been added.
		self.the_database = self.load_db()

	# The load_db() method initializes the_database. It's called when the database object
	# is first created and whenever new movie info is added by the user.
	def create_db(self):

		engine = create_engine("sqlite:///bmdb.db")

		metadata = MetaData()

		movie = Table('movie', metadata,
					  Column('id', Integer, primary_key=True),
					  Column('title', String),
					  Column('year', Integer)
					 )

		director = Table('director', metadata,
						 Column('id', Integer, primary_key=True),
						 Column('first_name', String),
						 Column('last_name', String),
						 Column('fullname', String)
						)

		actor = Table('actor', metadata,
					  Column('id', Integer, primary_key=True),
					  Column('first_name', String),
					  Column('last_name', String),
					  Column('fullname', String)
					 )

		format = Table('format', metadata,
					   Column('id', Integer, primary_key=True),
					   Column('format_type', String)
					  )

		genre = Table('genre', metadata,
					  Column('id', Integer, primary_key=True),
					  Column('genre_name', String)
					 )

		movie_director = Table('movie_director', metadata,
							   Column('movie_id', Integer),
							   Column('director_id', Integer)
							  )

		movie_actor = Table('movie_actor', metadata,
							Column('movie_id', Integer),
							Column('actor_id', Integer)
						   )

		movie_format = Table('movie_format', metadata,
							 Column('movie_id', Integer),
							 Column('format_id', Integer)
							)

		movie_genre = Table('movie_genre', metadata,
							Column('movie_id', Integer),
							Column('genre_id', Integer)
						   )

		metadata.create_all(engine)
	# The list_formatter() method takes an unformatted 2D list and returns a formatted 2D list
	# with the first letter of every word capitolized. Unformatted lists are for searching while
	# formatted lists are for printing and displaying.
	def list_formatter(self, list_2D):

		formatted_list = [[[None] for i in range (6)] for i in range(len(list_2D))]
		for i in range(len(list_2D)):
			# Fill the temporary list with one set of movie data.
			for j in range(6):
				element = list_2D[i][j]
				if element == "n/a":
					element = element.upper()
				else:
					element = " ".join(word[0].upper() + word[1:].lower() for word in element.split())
				formatted_list[i][j] = element
		return formatted_list

	# The list_builder() method takes a 1D list of movie data and an integer value as arguments
	# and returns a 2D list of sorted movie data. The num_items argument tells list_builder() how
	# many categories per movie when creating the 2D list.
	def list_builder(self, list_1D, num_items):

		# num_groups determines how many movies the list will hold.
		num_groups = len(list_1D) / num_items

		# Here we create a 2D list which will hold all of our movie data. A 2D list
		# provides us with an intuitive organizational structure for searching and
		# adding movies to the database.
		list_2D = [[[None] for i in range(num_items)] for i in range(num_groups)]
		for i in range(num_groups):
			for j in range(num_items):
				word = list_1D.pop(0)
				list_2D[i][j] = word
		# Sort the list by alphabetical order.
		list_2D.sort()
		return list_2D

	def save_db(self, list_2D):
		pass

	def delete_entries(self, del_movie_dict):
		pass

#-----------------------------------------------------------------------------------------------------------
movies = Database()
movies.create_db()