try:
	from setuptools import setup
except ImportError:
	from disutils.core import setup

config = {
	'description': 'Provide schedule and grades for CIS90',
	'author': 'sam tindell',
	'download_url': '@github',
	'author_email': 'sjtindell@gmail',
	'version': '0.1',
	'install_requires': ['nose', 'BeautifulSoup4', 'requests'],
	'packages': ['src', 'tests'],
	'scripts': [],
	'name': 'check-grades'
}

setup(**config)
