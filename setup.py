try:
	from setuptools import setup
except ImportError:
	from disutils.core import setup

config = {
	'description': 'Class grades/scheduler',
	'author': 'sam tindell',
	'download_url': '@github',
	'author_email': 'sjtindell@gmail',
	'version': '0.1',
	'install_requires': ['nose'],
	'packages': ['src'],
	'scripts': [],
	'name': 'pyStudent'
}

setup(**config)
