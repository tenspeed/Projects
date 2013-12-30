# bmdb.py version 3.0
# Written by Todd Smith
# 10/15/2013
# Licence:
#		This file is released under the Lesser GNU Public License.
#
#-----------------------------------------------------------------------------------------------------------

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, mapper, relationship, Session

Base = declarative_base()

############################################################################################################
class Movie(Base):
	"""Movie Class"""
	
	__tablename__ = "movie"

	movie_id = Column(Integer, primary_key=True)
	title = Column(String(20), nullable=False)
	year = Column(Integer, nullable=False)
	movie_actor = relationship("MovieActor", cascade="all, delete-orphan", backref="movie")

	def __init__(self, title, year):
		self.title = title
		self.year = year

	def __repr__(self):
		return "<Movie('%s', '%s')>" % (self.title, self.year)


############################################################################################################
class Actor(Base):
	"""Actor Class"""

	__tablename__ = "actor"

	actor_id = Column(Integer, primary_key=True)
	first_name = Column(String(20), nullable=False)
	last_name = Column(String(20), nullable=False)

	def __init__(self, first_name, last_name):
		self.first_name = first_name
		self.last_name = last_name

	def __repr__(self):
		return "<Actor('%s', '%s')>" % (self.first_name, self.last_name)

############################################################################################################
class MovieActor(Base):
	"""MovieActor Association Class"""

	__tablename__ = "movieactor"
	movie_id = Column(Integer, ForeignKey('movie.movie_id'), primary_key=True)
	actor_id = Column(Integer, ForeignKey('actor.actor_id'), primary_key=True)

	def __init__(self, actor):
		self.actor = actor
	actor = relationship(Actor, lazy='joined')

#class Format(Base):
#	pass

# This is the Database class. The Database class handles any task relating to the movie database including,
# opening the file where the movie information is stored, searching for movies based on search criteria,
# and adding new movies to the database.
class Database(object):

	# Upon instantiation, a permanent database property is created by calling the load_db() method.
	def __init__(self):
		pass
	# The search() method accepts a query in the form of a string as an argument and
	# searches through the movie database looking for other strings that match or are
	# a partial match to the query. If a match is found, search() returns a formated,
	# 2D list of all the matching movie information.
	def search(self, query):
		pass

	# The add_new() method accepts a dictionary of new movie information to add to the
	# database. add_new() check for duplicates and then if none are found, writes the new
	# movie information to bmdb.txt and reinitializes the_database.
	def add_new(self, new_movie_list):

		keys = ['title', 'genre', 'director', 'year', 'format', 'actors']

#-----------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	engine = create_engine('sqlite:///bmdb.db', echo=True)
	Base.metadata.create_all(engine)

	session = Session(engine)

	#add some actors to the Actor table
	brad_pitt = Actor('brad', 'pitt')
	edward_norton = Actor('edward', 'norton')

	#add a movie to the Movie table
	fight_club = Movie('fight club', 1999)

	fight_club.movie_actor.append(MovieActor(brad_pitt))
	fight_club.movie_actor.append(MovieActor(edward_norton))

	session.add(fight_club)
	session.commit()

	world_war_z = Movie('world war z', 2013)

	mireille_enos = Actor('mireille', 'enos')

	world_war_z.movie_actor.append(MovieActor(brad_pitt))
	world_war_z.movie_actor.append(MovieActor(mireille_enos))

	session.add(world_war_z)
	session.commit()

	q = session.query(Movie).filter(and_(Actor.first_name == 'brad'),
										Actor.actor_id == MovieActor.actor_id,
										Movie.movie_id == MovieActor.movie_id)

	for movie in q:
		print movie

	q = session.query(Movie).filter(and_(Actor.first_name == 'mireille'),
										 Actor.actor_id == MovieActor.actor_id,
										 Movie.movie_id == MovieActor.movie_id)

	for movie in q:
		print movie