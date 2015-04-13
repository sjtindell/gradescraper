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

def remaining_weeks():	
	print 'args:', sys.argv
	print 'calling schedule func...'
	#url = 'http://simms-teach.com/cis90calendar.php'
	#calendar = scraper.calendar_page(url)
	interface.display_schedule()

def user_grades():
	print 'args:', sys.argv
	print 'calling grades funcs...'
	data = UserData(sys.argv[2])
	interface.display_user_summary(data)
	see_more()
	interface.display_user_scores(data)
	see_more()
	interface.display_user_points_until(data)
	see_more()
	interface.display_remaining_points(data)


if sys.argv[1] == 'schedule':
	remaining_weeks()
elif sys.argv[1] == 'grades':
	try:
		user_grades()
	except:
		print '-' * 10
		print 'Unexpected argument.'
