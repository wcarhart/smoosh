'''
smoosh
------
Summarize any text article into just a few sentences. Try it out with `smoosh <url>`.
Repo: https://github.com/wcarhart/smoosh
'''
import os
from setuptools import setup, find_packages

def read(filename):
	with open(os.path.join(os.path.dirname(__file__), filename)) as f:
		return f.read()

setup(
	name='smoosh',
	version='2.1.0',
	description='Summarize any text article',
	long_description=__doc__,
	author='Will Carhart',
	url='https://github.com/wcarhart/smoosh',
	license='MIT',
	platforms='any',
	packages=find_packages(),
	install_requires=read('requirements.txt').splitlines(),
	zip_safe=False,
	entry_points={'console_scripts': ['smoosh = smoosh:main']}
)