from nose.tools import *
from bin.app import app
from tests.tools import assert_response
from tmdb.tmdb import Database

def test_index():
	# check that we get a 303 on the / URL
	resp = app.request("/")
	assert_response(resp, status="303")

	# test our first GET request to /main
	resp = app.request("/main")
	assert_response(resp)

def test_search():
	pass
	# check that we get a 200 on the /search URL
	#resp = app.request("/search")
	#assert_response(resp, status="200")

	# make sure default values work for the form
	#resp = app.request("/search", method="POST")
	#assert_response(resp, contains=None)

	# test that we get expected values
	#data = {'query': 'pacific rim'}
	#resp = app.request("/search", method="POST", data=data)
	#assert_response(resp, contains="pacific rim")