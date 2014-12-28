# bmdb.py version 3.1
# Written by Todd Smith
# 10/15/2013
# Licence:
#                This file is released under the Lesser GNU Public License.
#
#-----------------------------------------------------------------------------------------------------------
from sqlalchemy import Table, Column, Integer, String, ForeignKey, create_engine, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, Session

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
        movie_actor = relationship("MovieActor", cascade="all, delete-orphan", backref="movie")
        movie_director = relationship("MovieDirector", cascade="all, delete-orphan", backref="movie")
        movie_genre = relationship("MovieGenre", cascade="all, delete-orphan", backref="movie")

        def __init__(self, title, year, format):
                self.title = title
                self.year = year
                self.format = format

        def __repr__(self):
                return "<Movie(movie_id='%d', title='%s', year='%d', format='%s')>" % (self.movie_id, self.title, self.year, self.format)

############################################################################################################
class Actor(Base):
        """Actor Class"""

        __tablename__ = "actor"

        actor_id = Column(Integer, primary_key=True)
        full_name = Column(String(30), nullable=False, unique=True)

        def __init__(self, full_name):
                self.full_name = full_name

        def __repr__(self):
                return "<Actor(actor_id='%d', full_name='%s')>" % (self.actor_id, self.full_name)

############################################################################################################
class Director(Base):
        """Director Class"""

        __tablename__ = "director"

        director_id = Column(Integer, primary_key=True)
        full_name = Column(String(30), nullable=False, unique=True)

        def __init__(self, full_name):
                self.full_name = full_name

        def __repr__(self):
                return "<Director(director_id='%d', full_name='%s')>" % (self.director_id, self.full_name)

############################################################################################################
class Genre(Base):
        """Genre Class"""

        __tablename__ = "genre"

        genre_id = Column(Integer, primary_key=True)
        genre_name = Column(String(60), nullable=False, unique=True)

        def __init__(self, genre_name):
                self.genre_name = genre_name

        def __repr__(self):
                return "<Genre(genre_id='%d', genre_name='%s')>" % (self.genre_id, self.genre_name)

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
                return "<MovieActor(movie_id='%d', actor_id='%d')>" % (self.movie_id, self.actor_id)

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
                return "<MovieDirector(movie_id='%d', director_id='%d')>" % (self.movie_id, self.director_id)

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
                return "<MovieGenre(movie_id='%d', genre_id='%d')>" % (self.movie_id, self.genre_id)

############################################################################################################
# This is the Database class. The Database class queries the database, adds new movie data to the database,
# deletes records from the database, and returns/formats movie data for display to the user.
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
        def search(self, query_dict):
                # initialize the movie list and some strings
                movie_list = []
                actor_string = ""
                director_string = ""
                genre_string = ""
                
                # this block of code determines if the query submitted is a movie title, actor, director, or genre and then
                # builds a list of results to display
                try:
                    if query_dict['title']:
                        # for each title in the list, capitalize the first letter of each word in the title to match the formatting
                        # of the data in the SQL database
                        query_title = query_dict['title']
                        query_title = " ".join(word[0].upper() + word[1:].lower() for word in query_title.split())
                        t = self.session.query(Movie).filter(Movie.title == query_title).all()   
                        for i in range(len(t)):
                            # find all the actors which star in the current movie
                            a = self.session.query(Actor).filter(and_(Movie.title == t[i].title,
                                                                      Movie.movie_id == MovieActor.movie_id,
                                                                      Actor.actor_id == MovieActor.actor_id))
                            # construct one long string of all the actors separated by commas
                            for record in a:
                                    actor_string += record.full_name
                                    actor_string += ", "

                            # remove the last comma/space at the end of the string
                            actor_string = actor_string[:-1]
                            actor_string = actor_string[:-1]

                            # find all the directors associated with the current movie
                            d = self.session.query(Director).filter(and_(Movie.title == t[i].title,
                                                                         Movie.movie_id == MovieDirector.movie_id,
                                                                         Director.director_id == MovieDirector.director_id))
                            # construct one long string of all the directors separated by commas
                            for record in d:
                                    director_string += record.full_name
                                    director_string += ", "

                            # remove the last comma/space at the end of the string
                            director_string = director_string[:-1]
                            director_string = director_string[:-1]

                            # find all the genres associated with the current movie
                            g = self.session.query(Genre).filter(and_(Movie.title == t[i].title,
                                                                      Movie.movie_id == MovieGenre.movie_id,
                                                                      Genre.genre_id == MovieGenre.genre_id))
                            # construct one long string of all the genres separated by commas
                            for record in g:
                                    genre_string += record.genre_name
                                    genre_string += ", "

                            # remove the last comma/space at the end of the string
                            genre_string = genre_string[:-1]
                            genre_string = genre_string[:-1]

                            # movie_list = ['title', 'genre', 'year', 'director', 'actors', 'format']
                            # append all the relevent movie, actor, director, and genre info to the movie_list
                            movie_list.append(t[i].title)
                            movie_list.append(genre_string)
                            movie_list.append(t[i].year)
                            movie_list.append(director_string)
                            movie_list.append(actor_string)
                            movie_list.append(t[i].format)

                            # clear the temporary strings
                            actor_string = ""
                            director_string = ""
                            genre_string = ""
            
                        # format the 1D list into a 2D list
                        movie_list = self.list_builder(movie_list, 6)
                        return movie_list
                    else:
                        t = None

                    if query_dict['genre']:
                        # for each genre in the list, capitalize the first letter of each word in the genre
                        query_genre = query_dict['genre']
                        query_genre = " ".join(word[0].upper() + word[1:].lower() for word in query_genre.split())
                        g = self.session.query(Genre).filter(Genre.genre_name == query_genre).all()   
                        for i in range(len(g)):
                            # find all the movies associated with the current genre
                            t = self.session.query(Movie).filter(and_(Genre.genre_name == g[i].genre_name,
                                                                      Movie.movie_id == MovieGenre.movie_id,
                                                                      Genre.genre_id == MovieGenre.genre_id))
                        for title_record in t:

                            # find all the actors which star in the current movie
                            a = self.session.query(Actor).filter(and_(Movie.title == title_record.title,
                                                                      Movie.movie_id == MovieActor.movie_id,
                                                                      Actor.actor_id == MovieActor.actor_id))
                            # construct one long string of all the actors separated by commas
                            for record in a:
                                    actor_string += record.full_name
                                    actor_string += ", "

                            # remove the last comma/space at the end of the string
                            actor_string = actor_string[:-1]
                            actor_string = actor_string[:-1]

                            # find all the directors associated with the current movie
                            d = self.session.query(Director).filter(and_(Movie.title == title_record.title,
                                                                         Movie.movie_id == MovieDirector.movie_id,
                                                                         Director.director_id == MovieDirector.director_id))
                            # construct one long string of all the directors separated by commas
                            for record in d:
                                    director_string += record.full_name
                                    director_string += ", "

                            # remove the last comma/space at the end of the string
                            director_string = director_string[:-1]
                            director_string = director_string[:-1]

                            # find all the genres associated with the current movie
                            g = self.session.query(Genre).filter(and_(Movie.title == title_record.title,
                                                                      Movie.movie_id == MovieGenre.movie_id,
                                                                      Genre.genre_id == MovieGenre.genre_id))
                            # construct one long string of all the genres separated by commas
                            for record in g:
                                    genre_string += record.genre_name
                                    genre_string += ", "

                            # remove the last comma/space at the end of the string
                            genre_string = genre_string[:-1]
                            genre_string = genre_string[:-1]

                            # movie_list = ['title', 'genre', 'year', 'director', 'actors', 'format']
                            # append all the relevent movie, actor, director, and genre info to the movie_list
                            movie_list.append(title_record.title)
                            movie_list.append(genre_string)
                            movie_list.append(title_record.year)
                            movie_list.append(director_string)
                            movie_list.append(actor_string)
                            movie_list.append(title_record.format)

                            # clear the temporary strings
                            actor_string = ""
                            director_string = ""
                            genre_string = ""
            
                        # format the 1D list into a 2D list
                        movie_list = self.list_builder(movie_list, 6)
                        return movie_list

                    else:
                        g = None

                    if query_dict['actors']:
                        # for each actor in the list, capitalize the first letter of each word in the actor name
                        query_actors = query_dict['actors']
                        query_actors = " ".join(word[0].upper() + word[1:].lower() for word in query_actors.split())
                        a = self.session.query(Actor).filter(Actor.full_name == query_actors).all()   
                        for i in range(len(a)):
                            # find all the movies associated with the current genre
                            t = self.session.query(Movie).filter(and_(Actor.full_name == a[i].full_name,
                                                                      Movie.movie_id == MovieActor.movie_id,
                                                                      Actor.actor_id == MovieActor.actor_id))
                        for title_record in t:

                            # find all the actors which star in the current movie
                            a = self.session.query(Actor).filter(and_(Movie.title == title_record.title,
                                                                      Movie.movie_id == MovieActor.movie_id,
                                                                      Actor.actor_id == MovieActor.actor_id))
                            # construct one long string of all the actors separated by commas
                            for record in a:
                                    actor_string += record.full_name
                                    actor_string += ", "

                            # remove the last comma/space at the end of the string
                            actor_string = actor_string[:-1]
                            actor_string = actor_string[:-1]

                            # find all the directors associated with the current movie
                            d = self.session.query(Director).filter(and_(Movie.title == title_record.title,
                                                                         Movie.movie_id == MovieDirector.movie_id,
                                                                         Director.director_id == MovieDirector.director_id))
                            # construct one long string of all the directors separated by commas
                            for record in d:
                                    director_string += record.full_name
                                    director_string += ", "

                            # remove the last comma/space at the end of the string
                            director_string = director_string[:-1]
                            director_string = director_string[:-1]

                            # find all the genres associated with the current movie
                            g = self.session.query(Genre).filter(and_(Movie.title == title_record.title,
                                                                      Movie.movie_id == MovieGenre.movie_id,
                                                                      Genre.genre_id == MovieGenre.genre_id))
                            # construct one long string of all the genres separated by commas
                            for record in g:
                                    genre_string += record.genre_name
                                    genre_string += ", "

                            # remove the last comma/space at the end of the string
                            genre_string = genre_string[:-1]
                            genre_string = genre_string[:-1]

                            # movie_list = ['title', 'genre', 'year', 'director', 'actors', 'format']
                            # append all the relevent movie, actor, director, and genre info to the movie_list
                            movie_list.append(title_record.title)
                            movie_list.append(genre_string)
                            movie_list.append(title_record.year)
                            movie_list.append(director_string)
                            movie_list.append(actor_string)
                            movie_list.append(title_record.format)

                            # clear the temporary strings
                            actor_string = ""
                            director_string = ""
                            genre_string = ""
            
                        # format the 1D list into a 2D list
                        movie_list = self.list_builder(movie_list, 6)
                        return movie_list

                    else:
                        a = None    

                    if query_dict['director']:
                        # for each director in the list, capitalize the first letter of each word in the director name
                        query_director = query_dict['director']
                        query_director = " ".join(word[0].upper() + word[1:].lower() for word in query_director.split())
                        d = self.session.query(Director).filter(Director.full_name == query_director).all()   
                        for i in range(len(d)):
                            # find all the movies associated with the current director
                            t = self.session.query(Movie).filter(and_(Director.full_name == d[i].full_name,
                                                                      Movie.movie_id == MovieDirector.movie_id,
                                                                      Director.director_id == MovieDirector.director_id))
                        for title_record in t:

                            # find all the actors which star in the current movie
                            a = self.session.query(Actor).filter(and_(Movie.title == title_record.title,
                                                                      Movie.movie_id == MovieActor.movie_id,
                                                                      Actor.actor_id == MovieActor.actor_id))
                            # construct one long string of all the actors separated by commas
                            for record in a:
                                    actor_string += record.full_name
                                    actor_string += ", "

                            # remove the last comma/space at the end of the string
                            actor_string = actor_string[:-1]
                            actor_string = actor_string[:-1]

                            # find all the directors associated with the current movie
                            d = self.session.query(Director).filter(and_(Movie.title == title_record.title,
                                                                         Movie.movie_id == MovieDirector.movie_id,
                                                                         Director.director_id == MovieDirector.director_id))
                            # construct one long string of all the directors separated by commas
                            for record in d:
                                    director_string += record.full_name
                                    director_string += ", "

                            # remove the last comma/space at the end of the string
                            director_string = director_string[:-1]
                            director_string = director_string[:-1]

                            # find all the genres associated with the current movie
                            g = self.session.query(Genre).filter(and_(Movie.title == title_record.title,
                                                                      Movie.movie_id == MovieGenre.movie_id,
                                                                      Genre.genre_id == MovieGenre.genre_id))
                            # construct one long string of all the genres separated by commas
                            for record in g:
                                    genre_string += record.genre_name
                                    genre_string += ", "

                            # remove the last comma/space at the end of the string
                            genre_string = genre_string[:-1]
                            genre_string = genre_string[:-1]

                            # movie_list = ['title', 'genre', 'year', 'director', 'actors', 'format']
                            # append all the relevent movie, actor, director, and genre info to the movie_list
                            movie_list.append(title_record.title)
                            movie_list.append(genre_string)
                            movie_list.append(title_record.year)
                            movie_list.append(director_string)
                            movie_list.append(actor_string)
                            movie_list.append(title_record.format)

                            # clear the temporary strings
                            actor_string = ""
                            director_string = ""
                            genre_string = ""
            
                        # format the 1D list into a 2D list
                        movie_list = self.list_builder(movie_list, 6)
                        return movie_list
                    else:
                        d = None

                except TypeError:
                    return movie_list

                return None

        # view_collection method
        def view_collection(self):
                # create a temporary list to hold movie info for viewing
                movie_list = []
                #create temporary strings to put actor, director, and genre info into for viewing
                actor_string = ""
                director_string = ""
                genre_string = ""

                # query the database for all movies in the Movie table
                t = self.session.query(Movie).all()

                for i in range(len(t)):
                        # find all the actors which star in the current movie
                        a = self.session.query(Actor).filter(and_(Movie.title == t[i].title,
                                                                  Movie.movie_id == MovieActor.movie_id,
                                                                  Actor.actor_id == MovieActor.actor_id))
                        # construct one long string of all the actors separated by commas
                        for record in a:
                                actor_string += record.full_name
                                actor_string += ", "

                        # remove the last comma/space at the end of the string
                        actor_string = actor_string[:-1]
                        actor_string = actor_string[:-1]

                        # find all the directors associated with the current movie
                        d = self.session.query(Director).filter(and_(Movie.title == t[i].title,
                                                                     Movie.movie_id == MovieDirector.movie_id,
                                                                     Director.director_id == MovieDirector.director_id))
                        # construct one long string of all the directors separated by commas
                        for record in d:
                                director_string += record.full_name
                                director_string += ", "

                        # remove the last comma/space at the end of the string
                        director_string = director_string[:-1]
                        director_string = director_string[:-1]

                        # find all the genres associated with the current movie
                        g = self.session.query(Genre).filter(and_(Movie.title == t[i].title,
                                                                  Movie.movie_id == MovieGenre.movie_id,
                                                                  Genre.genre_id == MovieGenre.genre_id))
                        # construct one long string of all the genres separated by commas
                        for record in g:
                                genre_string += record.genre_name
                                genre_string += ", "

                        # remove the last comma/space at the end of the string
                        genre_string = genre_string[:-1]
                        genre_string = genre_string[:-1]

                        # movie_list = ['title', 'genre', 'year', 'director', 'actors', 'format']
                        # append all the relevent movie, actor, director, and genre info to the movie_list
                        movie_list.append(t[i].title)
                        movie_list.append(genre_string)
                        movie_list.append(t[i].year)
                        movie_list.append(director_string)
                        movie_list.append(actor_string)
                        movie_list.append(t[i].format)

                        # clear the temporary strings
                        actor_string = ""
                        director_string = ""
                        genre_string = ""
        
                # format the 1D list into a 2D list
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
                                # construct one long string of all the formats that turn up, separated by commas
                                format += new_movie[formats[str(i)]]
                                format += ", "
                        except:
                                pass

                # remove the last comma/space from the format string
                format = format[:-1]
                format = format[:-1]
                # capitalize the first letter of each word in the movie title
                title = " ".join(word[0].upper() + word[1:].lower() for word in new_movie['title'].split())
                # query the database to see if the movie already exists in the Movie table
                movie = self.session.query(Movie).filter(Movie.title == title).first()
                # if the movie already exists, leave add_new() without updating the database
                if movie:
                    return None
                # if the movie isn't already in the database, add it to the Movie table
                movie = Movie(title, new_movie['year'], format)
               
                # parse the text in the actors dictionary
                # take the incoming string of all actors in the movie and split it into a list of individual actors
                actors = new_movie['actors'].split(", ")        
                for i in range(len(actors)):
                        # for each actor in the list, capitalize the first letter in their first and last names
                        actors[i] = " ".join(word[0].upper() + word[1:].lower() for word in actors[i].split())
                        # query the database to see if the current actor already exists in the Actor table
                        actor = self.session.query(Actor).filter(Actor.full_name == actors[i]).first()
                        # if the actor already exists, create the movie/actor relation in the MovieActor table
                        if actor:
                            movie.movie_actor.append(MovieActor(actor))
                        # if the actor doesn't already exist, add it to the Actor table and create the movie/actor relation
                        # in the MovieActor table
                        else:
                            actor = Actor(actors[i])
                            movie.movie_actor.append(MovieActor(actor))
                                
                # parse the text in the directors dictionary
                # take the incoming string of all the directors associated with the movie and split it into a list
                # of individual directors
                directors = new_movie['director'].split(", ")
                for i in range(len(directors)):
                        # for each director in the list, capitalize the first letter in their first and last names
                        directors[i] = " ".join(word[0].upper() + word[1:].lower() for word in directors[i].split())
                        # query the database to see if the current director already exists in the Director table
                        director = self.session.query(Director).filter(Director.full_name == directors[i]).first()
                        # if the director already exists, create the movie/director relation in the MovieDirector table
                        if director:
                            movie.movie_director.append(MovieDirector(director))
                        # if the director doesn't already exist, add it to the Director table and create the movie/director
                        # relation in the MovieDirector table
                        else:
                            director = Director(directors[i])
                            movie.movie_director.append(MovieDirector(director))

                # parse the text in the genre dictionary
                genres = new_movie['genre'].split(", ")
                for i in range(len(genres)):
                        # for each genre in the list, capitalize the first letter
                        genres[i] = " ".join(word[0].upper() + word[1:].lower() for word in genres[i].split())
                        # query the database to see if the current genre already exists in the Genre table
                        genre = self.session.query(Genre).filter(Genre.genre_name == genres[i]).first()
                        # if the genre already exists, create the movie/genre relation in the MovieGenre table
                        if genre:
                            movie.movie_genre.append(MovieGenre(genre))
                        # if the genre doesn't already exist, add it to the Genre table and create the movie/genre relation
                        # in the MovieGenre table
                        else:
                            genre = Genre(genres[i])
                            movie.movie_genre.append(MovieGenre(genre))

                        # add and commit the new movie data
                        self.session.add(movie)
                        self.session.commit()
                return None

        def delete_movie(self, movie_input):
            delete_me = movie_input['title']
            delete_me = " ".join(word[0].upper() + word[1:].lower() for word in delete_me.split())
            t = self.session.query(Movie).filter(Movie.title == delete_me).one()
            self.session.delete(t)
            self.session.commit()
            return None

        def db_test(self):
            actor_list =[]

            all_actors = self.session.query(Actor).all()

            for record in all_actors:
                actor_list.append(record.full_name)
            actor_list.sort()
            for i in range(len(actor_list)):
                print actor_list[i]





############################################################################################################
#Testing Section
"""
engine = create_engine('sqlite:///bmdb.db')
Base.metadata.create_all(engine)
session = Session(engine)

#add some actors to the Actor table
brad_pitt = Actor('brad pitt')
edward_norton = Actor('edward norton')

#add a movie to the Movie table
fight_club = Movie('fight club', 1999, '2')

#add a director to the Director table
david_fincher = Director('david fincher')

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

mireille_enos = Actor('mireille enos')

marc_forster = Director('marc forster')

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

q = session.query(Movie, Director).filter(and_(Actor.full_name == 'mireille enos',
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

q = session.query(MovieActor).all()
for record in q:
    print record
print "\n\n"

q = session.query(MovieDirector).all()
for record in q:
    print record
print "\n\n"

q = session.query(MovieGenre).all()
for record in q:
    print record
print "\n\n"

q = session.query(Movie).all()
for record in q:
    print record
print "\n\n"

q = session.query(Actor).all()
for record in q:
    print record
print "\n\n"

q = session.query(Director).all()
for record in q:
    print record
print "\n\n"

q = session.query(Genre).all()
for record in q:
    print record
print"\n\n"


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

q = session.query(MovieActor).all()
for record in q:
    print record
print "\n\n"

q = session.query(MovieDirector).all()
for record in q:
    print record
print "\n\n"

q = session.query(MovieGenre).all()
for record in q:
    print record
print "\n\n"


q = session.query(Movie).all()
for record in q:
    print record
print "\n\n"

q = session.query(Actor).all()
for record in q:
    print record
print "\n\n"

q = session.query(Director).all()
for record in q:
    print record
print "\n\n"

q = session.query(Genre).all()
for record in q:
    print record
print"\n\n"
"""