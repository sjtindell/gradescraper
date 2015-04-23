# check-grades

For convenience.
Scrape the class website and
provide grades/schedule information.

Opus Version

setup
- clone the repo; cd
- optional: virtualenv -p /usr/bin/python2.6
- pip install -r requirements.txt

tests
- nosetests

scripts in /bin
- schedule : get the remaining semester schedule
- grades : get the grades for arg[1] lotr name
- forums : browse the cis forums
- tips: get random Linux/Bash tips

.py module layout
- scraper -> formatter -> interface -> command_line for schedule/grades
- forums
- tips

readme todo:
TravisCI button w/state of build
Quickstart documentation
List of Non-Python dependencies
and how to install
