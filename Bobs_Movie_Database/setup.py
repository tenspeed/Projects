try:
	from setuptools import setup
except ImportError
	from distutils.core import setup

config = {
	'description': "Bob's Movie Database",
	'author': 'Todd Smith',
	'url': 'https://github.com/tenspeed',
	'download_url': 'N/A',
	'author_email': 'tsmith86@gmail.com',
	'version': '3.1'
	'install_requires': ['nose', 'Flask', 'SQLAlchemy'],
	'packages': ['NAME'],
	'scripts': [],
	'name': 'bmdb'
}

setup(**config)