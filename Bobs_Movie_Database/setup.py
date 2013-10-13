try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description': 'bmdb organizes movie collections into a searchable database',
	'author': 'Todd Smith',
	'url': 'https://github.com/tenspeed/Projects',
	'download_url': '',
	'author_email': 'tsmith86@gmail.com',
	'version': '1.1',
	'install_requires': ['nose'],
	'packages': ['bmdb'],
	'scripts': [],
	'name': 'bmdb'
}

setup(**config)