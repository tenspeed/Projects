# bmdb.py version 3.0
# Written by Todd Smith
# 10/15/2013
# Licence:
#                This file is released under the Lesser GNU Public License.
#
#-----------------------------------------------------------------------------------------------------------

from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, create_engine, and_, or_, select
from sqlalchemy.orm import Session, sessionmaker

metadata = MetaData()

formats = {'1': 'DVD', '2': 'Blu-ray', '3': 'Digital', '4': 'VHS'}

############################################################################################################
movie = Table('movie', metadata,
		Column('movie_id', Integer, primary_key=True),
		Column('title', String, nullable=False, unique=True),
		Column('year', Integer, nullable=False),
		Column('format', String, nullable=False)
		)

actor = Table('actor', metadata,
		Column('actor_id', Integer, primary_key=True),
		Column('full_name', String, nullable=False)
		)

director = Table('director', metadata,
		Column('director_id', Integer, primary_key=True),
		Column('full_name', String, nullable=False)
		)

genre = Table('genre', metadata,
		Column('genre_id', Integer, primary_key=True),
		Column('genre_name', String, nullable=False)
		)

movie_actor = Table('movie_actor', metadata,
		Column('movie_id', Integer, ForeignKey('movie.movie_id')),
		Column('actor_id', Integer, ForeignKey('actor.actor_id'))
		)

movie_director = Table('movie_director', metadata,
		Column('movie_id', Integer, ForeignKey('movie.movie_id')),
		Column('director_id', Integer, ForeignKey('director.director_id'))
		)

movie_genre = Table('movie_genre', metadata,
		Column('movie_id', Integer, ForeignKey('movie.movie_id')),
		Column('genre_id', Integer, ForeignKey('genre.genre_id'))
		)

############################################################################################################
class Database(object):
    # A connection to the movie database is established upon instantiation.
    def __init__(self):
        engine = create_engine('sqlite:///bmdb.db')
        Session = sessionmaker(bind=engine)
        self.conn = engine.connect()
        self.session = Session(bind=self.conn)


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
        pass

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
        ins = movie.insert().values(title=title, year=new_movie['year'], format=format)
        #try:
            # add the new movie to the session
        self.session.execute(ins)
        self.session.commit()
        #except:
        #    print "Duplicate Movie"

        # parse the text in the actors entry
        # take the incoming string of all actors in the movie and split it into a list of individual actors
        actor_list = new_movie['actors'].split(", ")        
        for i in range(len(actor_list)):
            # for each actor in the list, capitalize the first letter in their first and last names
            actor_list[i] = " ".join(word[0].upper() + word[1:].lower() for word in actor_list[i].split())
            ins = actor.insert().values(full_name=actor_list[i])
            try:
                # add the appropriate association between the movie and the actors to the MovieActor table
                self.session.execute(ins)
            except:
                print "Duplicate Actor"
            #sel = select([movie.c.movie_id]).where(movie.c.title == new_movie['title'])
            #m_id = self.session.execute(sel)
            #sel = select([actor.c.actor_id]).where(actor.c.full_name == actor_list[i])
            #a_id = self.session.execute(sel)
            #ins = movie_actor.insert().values(movie_id = m_id['movie_id'], actor_id = a_id['actor_id'])

        # parse the text in the directors entry
        director_list = new_movie['director'].split(", ")
        for i in range(len(director_list)):
            director_list[i] = " ".join(word[0].upper() + word[1:].lower() for word in director_list[i].split())
            ins = director.insert().values(full_name=director_list[i])
            try:
                self.session.execute(ins)
            except:
                print "Duplicate Director"

        # parse the text in the genre entry
        genre_list = new_movie['genre'].split(", ")
        for i in range(len(genre_list)):
    	    genre_list[i] = " ".join(word[0].upper() + word[1:].lower() for word in genre_list[i].split())
    	    ins = genre.insert().values(genre_name=genre_list[i])
            try:
                self.session.execute(ins)
            except:
                print "Duplicate Genre"

        sel = select([movie.c.movie_id, movie.c.title])
        m = self.session.execute(sel)
        sel = select([actor.c.actor_id, actor.c.full_name])
        a = self.session.execute(sel)
        sel = select([director.c.director_id, director.c.full_name])
        d = self.session.execute(sel)
        sel = select([genre.c.genre_id, genre.c.genre_name])
        g = self.session.execute(sel)
        sel = select([movie_actor.c.movie_id, movie_actor.c.actor_id])
        ma = self.session.execute(sel)

        for row in m:
            print row
        for row in a:
            print row
        for row in d:
            print row
        for row in g:
            print row
        for row in ma:
            print row



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