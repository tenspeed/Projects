# bmdb.py version 3.0
# Written by Todd Smith
# 10/15/2013
# Licence:
#                This file is released under the Lesser GNU Public License.
#
#-----------------------------------------------------------------------------------------------------------
from sqlalchemy import Table, Column, Integer, String, ForeignKey, create_engine, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, mapper, relationship, Session

Base = declarative_base()

formats = {'1': 'DVD', '2': 'Blu-ray', '3': 'Digital', '4': 'VHS'}

############################################################################################################
class Movie(Base):
        """Movie Class"""
        
        __tablename__ = "movie"

        movie_id = Column(Integer, primary_key=True)
        title = Column(String(20), nullable=False, unique=True)
        year = Column(Integer, nullable=False)
        format = Column(String, nullable=False)
        movie_actor = relationship("Actor", secondary="movieactor", backref="movie")
        #movie_actor = relationship("MovieActor", cascade="all, delete-orphan", backref="movie")
        movie_director = relationship("MovieDirector", cascade="all, delete-orphan", backref="movie")
        movie_genre = relationship("MovieGenre", cascade="all, delete-orphan", backref="movie")

        def __init__(self, title, year, format):
                self.title = title
                self.year = year
                self.format = format

        def __repr__(self):
                return "%s %s" % (self.movie_id, self.title)

############################################################################################################
class Actor(Base):
        """Actor Class"""

        __tablename__ = "actor"

        actor_id = Column(Integer, primary_key=True)
        full_name = Column(String(30), nullable=False, unique=True)

        def __init__(self, full_name):
                self.full_name = full_name

        def __repr__(self):
                return "%s %s" % (self.actor_id, self.full_name)

############################################################################################################
class Director(Base):
        """Director Class"""

        __tablename__ = "director"

        director_id = Column(Integer, primary_key=True)
        full_name = Column(String(30), nullable=False, unique=True)

        def __init__(self, full_name):
                self.full_name = full_name

        def __repr__(self):
                return "%s %s" % (self.director_id, self.full_name)

############################################################################################################
class Genre(Base):
        """Genre Class"""

        __tablename__ = "genre"

        genre_id = Column(Integer, primary_key=True)
        genre_name = Column(String(60), nullable=False, unique=True)

        def __init__(self, genre_name):
                self.genre_name = genre_name

        def __repr__(self):
                return "%s %s" % (self.genre_id, self.genre_name)

############################################################################################################
#class MovieActor(Base):
#        """MovieActor Association Class"""
#
#        __tablename__ = "movieactor"
#        movie_id = Column(Integer, ForeignKey('movie.movie_id'), primary_key=True)
#        actor_id = Column(Integer, ForeignKey('actor.actor_id'), primary_key=True)
#
#        def __init__(self, actor):
#                self.actor = actor
#        actor = relationship(Actor, lazy='joined')
#
#        def __repr__(self):
#                return "%s, %s" % (self.movie_id, self.actor_id)
MovieActor = Table('movieactor', Base.metadata,
        Column('movie_id', Integer, ForeignKey('movie.movie_id')),
        Column('actor_id', Integer, ForeignKey('actor.actor_id')))

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
                return "%s, %s" % (self.movie_id, self.director_id)

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
                return "%s, %s" % (self.movie_id, self.genre_id)

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

        # The list_builder() method takes a 1D list of movie data and an integer value as arguments
        # and returns a 2D list of sorted movie data. The num_items argument tells list_builder() how
        # many categories per movie when creating the 2D list.
        def list_builder(self, list_1D, num_items):

                # num_groups determines how many movies the list will hold.
                num_groups = len(list_1D) / num_items

                # Here we create a 2D list which will hold all of our movie data.
                list_2D = [[[None] for i in range(num_items)] for i in range(num_groups)]
                for i in range(num_groups):
                        for j in range(num_items):
                                word = list_1D.pop(0)
                                list_2D[i][j] = word
                # Sort the list by alphabetical order.
                list_2D.sort()
                return list_2D

        # search method
        def search(self, query):
                pass

        # view_collection method
        def view_collection(self):
                movie_list = []
                actor_string = ""
                director_string = ""
                genre_string = ""

                t = self.session.query(Movie).all()

                for i in range(len(t)):
                        a = self.session.query(Actor).filter(and_(Movie.title == t[i].title,
                                                                  Movie.movie_id == MovieActor.movie_id,
                                                                  Actor.actor_id == MovieActor.actor_id))
                        for record in a:
                                actor_string += record.full_name
                                actor_string += ", "

                        actor_string = actor_string[:-1]
                        actor_string = actor_string[:-1]

                        d = self.session.query(Director).filter(and_(Movie.title == t[i].title,
                                                                     Movie.movie_id == MovieDirector.movie_id,
                                                                     Director.director_id == MovieDirector.director_id))

                        for record in d:
                                director_string += record.full_name
                                director_string += ", "

                        director_string = director_string[:-1]
                        director_string = director_string[:-1]

                        g = self.session.query(Genre).filter(and_(Movie.title == t[i].title,
                                                                  Movie.movie_id == MovieGenre.movie_id,
                                                                  Genre.genre_id == MovieGenre.genre_id))

                        for record in g:
                                genre_string += record.genre_name
                                genre_string += ", "

                        genre_string = genre_string[:-1]
                        genre_string = genre_string[:-1]


                        # movie_list = ['title', 'genre', 'year', 'director', 'actors', 'format']
                        movie_list.append(t[i].title)
                        movie_list.append(genre_string)
                        movie_list.append(t[i].year)
                        movie_list.append(director_string)
                        movie_list.append(actor_string)
                        movie_list.append(t[i].format)

                        actor_string = ""
                        director_string = ""
                        genre_string = ""
        
                movie_list = self.list_builder(movie_list, 6)
                return movie_list

        # add_new method
        # takes a dictionary of strings containing all the info for a new movie: "title, actors, director, genre" etc
        # and formats the strings, then adds them to the proper tables in the database
        def add_new(self, new_movie):
                #find out what formats exist
                format = ""
                for i in range(1,5):
                        try:
                                format += new_movie[formats[str(i)]]
                                format += ", "
                        except:
                                pass

                format = format[:-1]
                format = format[:-1]
                # capitalize the first letter of each word in the movie title
                title = " ".join(word[0].upper() + word[1:].lower() for word in new_movie['title'].split())
                try:
                        movie = Movie(title, new_movie['year'], format)
                        # add the new movie to the session
                        self.session.add(movie)
                        # commit the new movie to the database
                        self.session.commit()
                except:
                        print "Duplicate Movie"
                        self.session.rollback()
                        return

                # parse the text in the actors entry
                # take the incoming string of all actors in the movie and split it into a list of individual actors
                actors = new_movie['actors'].split(", ")        
                for i in range(len(actors)):
                        # for each actor in the list, capitalize the first letter in their first and last names
                        actors[i] = " ".join(word[0].upper() + word[1:].lower() for word in actors[i].split())
                        # add each formatted actor name to the Actor table
                        actor = Actor(actors[i])
                        try:
                                # add the appropriate association between the movie and the actors to the MovieActor table
                                movie.movie_actor.append(actor)
                                #movie.movie_actor.append(MovieActor(actor))
                                # add the new movie to the session
                                self.session.add(movie)
                                # commit the new movie to the database
                                self.session.commit()
                        except:
                                print "Duplicate Actor"
                                self.session.rollback()
                                temp_assoc = MovieActor(movie_id = movie.movie_id, actor_id = actor.actor_id)
                                self.session.add(temp_assoc)
                                self.session.commit()

                # parse the text in the directors entry
                directors = new_movie['director'].split(", ")
                for i in range(len(directors)):
                        directors[i] = " ".join(word[0].upper() + word[1:].lower() for word in directors[i].split())
                        director = Director(directors[i])
                        try:
                                movie.movie_director.append(MovieDirector(director))
                                # add the new movie to the session
                                self.session.add(movie)
                                # commit the new movie to the database
                                self.session.commit()
                        except:
                                print "Duplicate Director"
                                self.session.rollback()

                # parse the text in the genre entry
                genres = new_movie['genre'].split(", ")
                for i in range(len(genres)):
                        genres[i] = " ".join(word[0].upper() + word[1:].lower() for word in genres[i].split())
                        genre = Genre(genres[i])
                        try:
                                movie.movie_genre.append(MovieGenre(genre))
                                # add the new movie to the session
                                self.session.add(movie)
                                # commit the new movie to the database
                                self.session.commit()
                        except:
                                print "Duplicate Genre"
                                self.session.rollback()

        		m = self.session.query(Movie).all()
        		a = self.session.query(Actor).all()
        		d = self.session.query(Director).all()
        		g = self.session.query(Genre).all()
        		ma = self.session.query(MovieActor).all()
        		md = self.session.query(MovieDirector).all()
        		mg = self.session.query(MovieGenre).all()

        		for record in m:
        			print "Movie table: ", record
        		for record in a:
        			print "Actor table: ", record
        		for record in d:
        			print "Director table: ", record
        		for record in g:
        			print "Genre table: ", record
        		for record in ma:
        			print "MovieActor table: ", record
        		for record in md:
        			print "MovieDirector table: ", record
        		for record in mg:
        			print "MovieGenre table: ", record

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