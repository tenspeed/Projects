from nose.tools import *
from bmdb.bmdb_orm import Database

def setup():
	print "SETUP!"

def teardown():
	print "TEAR DOWN!"

def test_basic():
	print "I RAN!"