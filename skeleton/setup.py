try:
	from setuptools import setuptools
except ImportError:
	from distutils.core import setuptools

config = {
	'description': 'My Project',
	'author': 'Todd Smith',
	'url': 'URL to get it at.',
	'download_url': 'Where to download it.',
	'author_email': 'tsmith86@gmail.com',
	'version': '0.1',
	'install_requires': ['nose'],
	'packages': ['NAME'],
	'scripts': [],
	'name': 'projectname'
}

setup(**config)