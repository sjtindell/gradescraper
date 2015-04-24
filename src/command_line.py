import sys

import interface
from formatter import UserData


def see_more():
	print
	more = raw_input('see more? y/n [y] ')
	print '-' * 10
	if more not in ('n', 'no'):
		pass
	else:
		sys.exit(0)

class BadArgument(Exception):
	pass


def user_grades():
	#print 'args:', sys.argv
	#print 'calling grades funcs...'
	#print 'should be user:', sys.argv[2]
	try:
		data = UserData(sys.argv[2])
		#print data
		interface.display_user_summary(data)
		see_more()
		interface.display_user_scores(data)
		see_more()
		interface.display_user_points_until(data)
		see_more()
		interface.display_remaining_points(data)
	except TypeError:
		print 'Invalid lotr name.'


if sys.argv[1] == 'schedule':
	#print 'args:', sys.argv
	#print 'calling schedule func...'
	#url = 'http://simms-teach.com/cis90calendar.php'
	#calendar = scraper.calendar_page(url)
	interface.display_schedule()
elif sys.argv[1] == 'grades':
	user_grades()
