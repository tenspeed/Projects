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

formats = {'1': "dvd", '2': "blu-ray", '3': "digital", '4': "vhs"}

############################################################################################################
class Movie(Base):
	"""Movie Class"""
	
	__tablename__ = "movie"

	movie_id = Column(Integer, primary_key=True)
	title = Column(String(20), nullable=False)
	year = Column(Integer, nullable=False)
	format_id = Column(String, nullable=False)
	movie_actor = relationship("MovieActor", cascade="all, delete-orphan", backref="movie")
	movie_director = relationship("MovieDirector", cascade="all, delete-orphan", backref="movie")
	movie_genre = relationship("MovieGenre", cascade="all, delete-orphan", backref="movie")

	def __init__(self, title, year, format_id):
		self.title = title
		self.year = year
		self.format_id = format_id

	def __repr__(self):
		return "<Movie('%s', '%s', '%s')>" % (self.title, self.year, self.format_id)

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
class Director(Base):
	"""Director Class"""

	__tablename__ = "director"

	director_id = Column(Integer, primary_key=True)
	first_name = Column(String(20), nullable=False)
	last_name = Column(String(20), nullable=False)

	def __init__(self, first_name, last_name):
		self.first_name = first_name
		self.last_name = last_name

	def __repr__(self):
		return"<Director('%s', '%s')>" % (self.first_name, self.last_name)

############################################################################################################
class Genre(Base):
	"""Genre Class"""

	__tablename__ = "genre"

	genre_id = Column(Integer, primary_key=True)
	genre_name = Column(String(60), nullable=False)

	def __init__(self, genre_name):
		self.genre_name = genre_name

	def __repr__(self):
		return"<Genre('%s')>" % (self.genre_name)

############################################################################################################
class MovieActor(Base):
	"""MovieActor Association Class"""

	__tablename__ = "movieactor"
	movie_id = Column(Integer, ForeignKey('movie.movie_id'), primary_key=True)
	actor_id = Column(Integer, ForeignKey('actor.actor_id'), primary_key=True)

	def __init__(self, actor):
		self.actor = actor
	actor = relationship(Actor, lazy='joined')

	def __repr__(self):
		return"<MovieActor('%s', '%s')>" % (self.movie_id, self.actor_id)

############################################################################################################
class MovieDirector(Base):
	"""MovieDirector Association Class"""

	__tablename__ = "moviedirector"
	movie_id = Column(Integer, ForeignKey('movie.movie_id'), primary_key=True)
	director_id = Column(Integer, ForeignKey('director.director_id'), primary_key=True)

	def __init__(self, director):
		self.director = director
	director = relationship(Director, lazy='joined')

	def __repr__(self):
		return"<MovieDirector('%s', '%s')>" % (self.movie_id, self.director_id)

############################################################################################################
class MovieGenre(Base):
	"""MovieGenre Association Class"""

	__tablename__ = "moviegenre"
	movie_id = Column(Integer, ForeignKey('movie.movie_id'), primary_key=True)
	genre_id = Column(Integer, ForeignKey('genre.genre_id'), primary_key=True)

	def __init__(self, genre):
		self.genre = genre
	genre = relationship(Genre, lazy='joined')

	def __repr__(self):
		return"<MovieGenre('%s', '%s')>" % (self.movie_id, self.genre_id)

############################################################################################################
# This is the Database class. The Database class handles any task relating to the movie database including,
# opening the file where the movie information is stored, searching for movies based on search criteria,
# and adding new movies to the database.
class Database(object):

	# A connection to the movie database is established upon instantiation.
	def __init__(self):
		engine = create_engine('sqlite:///bmdb.db')
		Base.metadata.create_all(engine)
		session = Session(engine)
		self.session = session

	# search method
	def search(self, query):
		pass

	# add_new method
	def add_new(self, new_movie):
		#find out what formats exist
		format = ""
		for i in range(1,5):
			try:
				format += new_movie[formats[str(i)]]
			except:
				pass

		movie = Movie(new_movie['title'].lower(), new_movie['year'], format)

		# parse the text in the actors entry
		actors = new_movie['actors'].split(", ")
		for i in range(len(actors)):
			single_actor = actors[i].split(" ")
			print "Actor #%d: %s %s" % (i+1, single_actor[0], single_actor[1]), "\n"
			actor = Actor(single_actor[0].lower(), single_actor[1].lower())
			movie.movie_actor.append(MovieActor(actor))

		# parse the text in the directors entry
		directors = new_movie['director'].split(", ")
		for i in range(len(directors)):
			single_director = directors[i].split(" ")
			print "Director #%d: %s %s" % (i+1, single_director[0], single_director[1]), "\n"
			director = Director(single_director[0].lower(), single_director[1].lower())
			movie.movie_director.append(MovieDirector(director))

		# parse the text in the genre entry
		single_genre = new_movie['genre'].split(", ")
		for i in range(len(single_genre)):
			print "Genre: %s" % (single_genre[i]), "\n"
			genre = Genre(single_genre[i].lower())
			movie.movie_genre.append(MovieGenre(genre))

		# add the new movie to the session
		self.session.add(movie)
		# commit the new movie to the database
		self.session.commit()

		q = self.session.query(Movie).filter(and_(Movie.title == new_movie['title'].lower()))

		for record in q:
			print record, "\n"

		q = self.session.query(Actor).filter(and_(Movie.title == new_movie['title'].lower(),
												  Movie.movie_id == MovieActor.movie_id,
												  Actor.actor_id == MovieActor.actor_id))
		for record in q:
			print record, "\n"

		q = self.session.query(Director).filter(and_(Movie.title == new_movie['title'].lower(),
													 Movie.movie_id == MovieDirector.movie_id,
													 Director.director_id == MovieDirector.director_id))
		for record in q:
			print record, "\n"

		q = self.session.query(Genre).filter(and_(Movie.title == new_movie['title'].lower(),
												  Movie.movie_id == MovieGenre.movie_id,
												  Genre.genre_id == MovieGenre.genre_id))
		for record in q:
			print record, "\n"


############################################################################################################
#Testing Section
"""
engine = create_engine('sqlite:///bmdb.db')
Base.metadata.create_all(engine)
session = Session(engine)

#add some actors to the Actor table
brad_pitt = Actor('brad', 'pitt')
edward_norton = Actor('edward', 'norton')

#add a movie to the Movie table
fight_club = Movie('fight club', 1999, '2')

#add a director to the Director table
david_fincher = Director('david', 'fincher')

#add a genre to the Genre table
drama = Genre('Drama')

#add the movie_id and actor_id's to the MovieActor table
fight_club.movie_actor.append(MovieActor(brad_pitt))
fight_club.movie_actor.append(MovieActor(edward_norton))

#add the movie_id and the director_id to the MovieDirector table
fight_club.movie_director.append(MovieDirector(david_fincher))

#add the movie_id and the genre_id to the MovieGenre table
fight_club.movie_genre.append(MovieGenre(drama))


session.add(fight_club)
session.commit()

world_war_z = Movie('world war z', 2013, '2')

mireille_enos = Actor('mireille', 'enos')

marc_forster = Director('marc', 'forster')

action = Genre('Action')
adventure = Genre('Adventure')
horror = Genre('Horror')

world_war_z.movie_actor.append(MovieActor(brad_pitt))
world_war_z.movie_actor.append(MovieActor(mireille_enos))
world_war_z.movie_director.append(MovieDirector(marc_forster))
world_war_z.movie_genre.append(MovieGenre(action))
world_war_z.movie_genre.append(MovieGenre(adventure))
world_war_z.movie_genre.append(MovieGenre(horror))

session.add(world_war_z)
session.commit()

print "\n\n"

q = session.query(Actor).filter(and_(Movie.title == 'fight club',
									Actor.actor_id == MovieActor.actor_id,
									Movie.movie_id == MovieActor.movie_id))

for movie in q:
	print movie
print "\n\n"

q = session.query(Movie, Director).filter(and_(Actor.first_name == 'mireille',
									 Actor.actor_id == MovieActor.actor_id,
									 Movie.movie_id == MovieActor.movie_id,
									 Director.director_id == MovieDirector.director_id,
									 Movie.movie_id == MovieDirector.movie_id))

for movie in q:
	print movie

print "\n\n"
print "number of movies in database: ", session.query(Movie).count()
print "number of directors in database: ", session.query(Director).count()
print "number of actors in database: ", session.query(Actor).count()
print "number of genres in database: ", session.query(Genre).count()
print "number of movie/director pairs: ", session.query(MovieDirector).count()
print "number of movie/actor pairs: ", session.query(MovieActor).count()
print "number of movie/genre pairs: ", session.query(MovieGenre).count()
print "\n\n"

print session.query(MovieActor).all(), "\n\n"
print session.query(MovieDirector).all(), "\n\n"
print session.query(MovieGenre).all(), "\n\n"


#delete World War Z from the database. What happens to the child tables?
session.delete(world_war_z)
session.commit()

print "\n\n"
print "number of movies in database: ", session.query(Movie).count()
print "number of directors in database: ", session.query(Director).count()
print "number of actors in database: ", session.query(Actor).count()
print "number of genres in database: ", session.query(Genre).count()
print "number of movie/director pairs: ", session.query(MovieDirector).count()
print "number of movie/actor pairs: ", session.query(MovieActor).count()
print "number of movie/genre pairs: ", session.query(MovieGenre).count()
print "\n\n"

print session.query(MovieActor).all(), "\n\n"
print session.query(MovieDirector).all(), "\n\n"
print session.query(MovieGenre).all(), "\n\n"

"""