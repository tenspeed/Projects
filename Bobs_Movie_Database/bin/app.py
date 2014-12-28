from flask import Flask, render_template, request, url_for, redirect
from bmdb import bmdb_orm

app = Flask(__name__)
moviedb = bmdb_orm.Database()

@app.route('/')
def index():
	return render_template('main.html')

@app.route('/search/', methods=['GET', 'POST'])
def search():
	if request.method == 'POST':
		form_data = request.form
		search_results = moviedb.search(form_data)
		if search_results == None:
			return render_template('main.html')
		else:
			num_items = len(search_results)
			return render_template('results.html', search_results=search_results, num_items=num_items, result_flag=0)
	else:
		return render_template('search.html', search_flag=0)

@app.route('/add/', methods=['GET', 'POST'])
def add():
	if request.method == 'POST':
		form_data = request.form
		moviedb.add_new(form_data)
		return redirect(url_for('add'))
	else:
		return render_template('add.html')

@app.route('/collection/')
def collection():
	search_results = moviedb.view_collection()
	num_items = len(search_results)
	return render_template('results.html', search_results=search_results, num_items=num_items, result_flag=0)

@app.route('/delete/', methods=['GET', 'POST'])
def delete():
	if request.method == 'POST':
		form_data = request.form
		search_results = moviedb.search(form_data)
		num_items = len(search_results)
		moviedb.delete_movie(form_data)
		return render_template('results.html', search_results=search_results, num_items=num_items, result_flag=1)
	else:
		return render_template('search.html', search_flag=1)


if __name__ == '__main__':
	app.run(debug=True)
