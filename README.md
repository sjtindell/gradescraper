# check-grades

For convenience.
Scrape the class website and
provide grades/schedule information.

v 0.1
May 2015
url: https://github.com/sjtindell/check-grades

Contributors:
Sam Tindell

setup
- clone the repo; cd
- optional: virtualenv -p /usr/bin/python2.6
- pip install -r requirements.txt

tests
- nosetests

scripts in /bin
- schedule : get the remaining semester schedule
- grades : get the grades for arg[1] lotr name

Layout
scraper -> formatter -> interface -> command_line -> schedule/grades scripts

readme todo:
TravisCI button w/state of build
