from flask import Flask, render_template, request, url_for, redirect
from bmdb import bmdb

app = Flask(__name__)
moviedb = bmdb.Database()

@app.route('/')
def index():
	return render_template('main.html')

@app.route('/search/', methods=['GET', 'POST'])
def search():
	if request.method == 'POST':
		form_data = request.form['query']
		return redirect(url_for('index'))
	else:
		return render_template('search.html')

@app.route('/add/', methods=['GET', 'POST'])
def add():
	if request.method == 'POST':
		form_data = request.form
		moviedb.add_new(form_data)
		return redirect(url_for('add'))
	else:
		return render_template('add.html')

@app.route('/collection/')
def results():
	moviedb.view_collection()
	#collection = moviedb.view_collection()
	#print (len(collection)/5)
	#print collection
	return render_template('results.html')#, collection=collection)

@app.route('/delete/')
def delete():
	return render_template('delete.html')


if __name__ == '__main__':
	app.run(debug=True)
#urls = (
#	'/main', 'Main_Menu',
#	'/search', 'Search',
#	'/add', 'Add_Movies',
#	'/view_collection', 'Collection',
#	'/', 'Index',
#	'/delete', 'Delete_Movies'
#	)

# Delete old sessions on start up
#folder = os.getcwd() + "\sessions"
#for the_file in os.listdir(folder):
#    file_path = os.path.join(folder, the_file)
#    try:
#    	os.unlink(file_path)
#    except Exception, e:
#        print e

#app = web.application(urls, globals())

# Little hack so that debug mode works with sessions.
#if web.config.get('_session') is None:
#	store = web.session.DiskStore('sessions')
#	session = web.session.Session(app, store,
#								  initializer={'db': None})
#	web.config._session = session
#else:
#	session = web.config._session

#render = web.template.render('templates/', base="layout")

#class Index(object):
#	def GET(self):
		# This is used to "setup" the session with starting values.
#		print "Calling session.db = bmdb.movies"
#		session.db = bmdb.Database()
#		print "Calling web.seeother('/main')"
#		web.seeother("/main")

#class Main_Menu(object):

#	def GET(self):
#		print "Calling render.main()"
#		return render.main()

#class Search(object):

#	def GET(self):
#		return render.search()

#	def POST(self):
#		form = web.input()
#		search_results = session.db.search(form.query)
#		return render.results(movie_list=search_results)

#class Add_Movies(object):

#	def GET(self):
#		return render.add()

#	def POST(self):
#		form = web.input()
#		session.db.add_new(form)
#		web.seeother("/add")

#class Collection(object):

#	def GET(self):
#		movie_list = session.db.list_formatter(session.db.the_database)
#		return render.results(movie_list=movie_list)

#class Delete_Movies(object):

#	def GET(self):
#		movie_list = session.db.list_formatter(session.db.the_database)
#		return render.delete(movie_list=movie_list)

#	def POST(self):
#		form = web.input()
#		session.db.delete_entries(form)
#		web.seeother("/main")

#if __name__ == "__main__":
#	app.run()