# This is a script to convert the old style bmdb text file into the new bmdb database

# bmdb text file convention: title; genres; directors; year; formats; actors;

# Open the text file where the movie information is saved and read it into the variable 'data'
# as a string.

from bmdb import bmdb_orm

moviedb = bmdb_orm.Database()

temp_dict = {'title': '', 'director': '', 'actors': '', 'genre': '', 'year': ''}

with open("bmdb_test.txt", 'a+') as f:
	data = f.read()

 # Remove the last ';' from the end of the string.
	data = data[:-1]

# put all the movie data into a list
movies = data.split(';')

# call the Database's list_builder method to put the movie data into an organized 2D list

movies = moviedb.list_builder(movies, 6)

for i in range(len(movies)):
	temp_dict['title'] = movies[i][0]
	temp_dict['genre'] = movies[i][1]
	temp_dict['director'] = movies[i][2]
	temp_dict['year'] = movies[i][3]
	temp_dict['actors'] = movies[i][5]

	formats = movies[i][4].split(',')

	if 'dvd' in formats:
		temp_dict['DVD'] = 'DVD'
	if 'bluray' in formats:
		temp_dict['Blu-ray'] = 'Blu-ray'
	if 'vhs' in formats:
		temp_dict['VHS'] = 'VHS'
	if 'digital' in formats:
		temp_dict['Digital'] = 'Digital'

	moviedb.add_new(temp_dict)

	if 'DVD' in temp_dict:	
		del temp_dict['DVD']
	if 'VHS' in temp_dict:
		del temp_dict['VHS']
	if 'Blu-ray' in temp_dict:
		del temp_dict['Blu-ray']
	if 'Digital' in temp_dict:
		del temp_dict['Digital']



