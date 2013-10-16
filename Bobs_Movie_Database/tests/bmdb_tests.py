from nose.tools import *
from bmdb.bmdb import Database

def test_list_builder():

	test_db = Database()
	test_list = test_db.list_builder(['one', 'two', 'three', 'four'], 2)
	assert_equal(test_list, [['one', 'two'], ['three', 'four']])
	test_list = test_db.list_builder(['one', 'two', 'three', 'four'], 1)
	assert_equal(test_list, [['four'], ['one'], ['three'], ['two']])

def test_list_formatter():

	test_db = Database()
	test_list = test_db.list_formatter([['one', 'two', 'three', 'four', 'five', 'six'],
										 ['seven', 'eight', 'nine', 'ten', 'eleven', 'twelve']])
	assert_equal(test_list, [['One', 'Two', 'Three', 'Four', 'Five', 'Six'],
								['Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve']])
	a_list = [['ThIs', 'THAT', 'whut', 'evEN', 'Is', 'SLKD'], ['IDUNNO', 'huH', 'HOw', 'blAh', 'bbBBaN', 'LaST onE BOY']]
	assert_equal(test_db.list_formatter(a_list), [['This', 'That', 'Whut', 'Even', 'Is', 'Slkd'], ['Idunno', 'Huh', 'How', 'Blah', 'Bbbban', 'Last One Boy']])

def test_search():
	
	test_db = Database()
	result = test_db.search('fight club')
	assert_equal(result, [['Fight Club', 'Drama', 'David Fincher', '1999', 'Dvd', 'Brad Pitt, Edward Norton']])
	result = test_db.search('jOSepH')
	assert_equal(result, [['10 Things I Hate About You', 'Comedy, Drama, Romance', 'Gil Junger', '1999', 'Dvd', 'Heath Ledger, Julia Stiles, Joseph Gordon-levitt'],
						  ['50/50', 'Comedy, Drama', 'Jonathan Levine', '2011', 'Dvd', 'Joseph Gordon-levitt, Seth Rogen, Anna Kendrick']])

def test_add_new():
	
	test_db = Database()
	new_movie = {'director': 'gaRy ROss', 'format': 'dVD', 'title': 'tHe HungEr Games', 'year': '2012', 'genre': 'Adventure, Sci-fi, thriLLer',
				 'actors': 'jennifer lawrence, JOSH HUTCHERSON, Liam Hemsworth'}
	test_db.add_new(new_movie)
	result = test_db.search('hunger games')
	assert_equal(result, [['The Hunger Games', 'Adventure, Sci-fi, Thriller', 'Gary Ross', '2012', 'Dvd', 'Jennifer Lawrence, Josh Hutcherson, Liam Hemsworth']])