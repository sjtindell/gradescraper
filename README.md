## Description
Scrape the class website and
provide grades/schedule information.
Also a phpbb forum browser and list
of bash tips/tricks.

## Versions
* 0.1 : May 2015
* 0.2 : September 2015

## Production Setup
- clone the repo
- pip install -r requirements.txt
- $ nosetests

## Development Setup
- clone the repo
- optional: virtualenv -p /usr/bin/python2.6
- pip install -r requirements.txt

## Tests
- nosetests

## Version-Control
- git


## Documentation
/lib
- scraper -> formatter -> interface -> command_line

Bash scripts in /bin enact the python interpreter and give the command_line
module arguments that provide the grades/schedule functionality.

/bin
- schedule : get the remaining semester schedule
- grades : get the grades for arg[1] lotr name
- forums : browse the class forum, can be modified for other phpbb forums
- tips : view random bash tips/tricks

## Contributors
Sam Tindell

