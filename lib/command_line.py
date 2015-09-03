import traceback
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


if sys.argv[1] == 'schedule':
	#print 'args:', sys.argv
	#print 'calling schedule func...'
	#url = 'http://simms-teach.com/cis90calendar.php'
	#calendar = scraper.calendar_page(url)
	interface.display_schedule()

elif sys.argv[1] == 'grades':
	
	try:
		user = sys.argv[2]
	except IndexError:
		print 'usage: grades <lotr name>'
		sys.exit(1)

	data = UserData(sys.argv[2])
	
	#print 'args:', sys.argv
	#print 'calling grades funcs...'
	#print 'should be user:', sys.argv[2]

	funcs = [
		interface.display_user_summary,
		#interface.display_user_scores,
		#interface.display_user_points_until,
		#interface.display_remaining_points
	]

			
	for iteration, func in enumerate(funcs):
		try:
			func(data)
		#except TypeError:
		#	print 'possibly invalid lotr name'
		#	sys.exit(1)
		except Exception as e:
			print 'exception:', e
			print 'Traceback:'
			ex_type, ex, tb = sys.exc_info()
			traceback.print_tb(tb)
			del(tb)
			print '-' * 10
			sys.exit(1)
		else:
			if iteration != 3:
				see_more()
