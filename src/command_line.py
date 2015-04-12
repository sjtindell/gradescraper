# take args, display views
# def display_see_more():
#	pass

# for testing
import sys
import interface


if sys.argv[1] == 'schedule':
	print 'args:', sys.argv
	print 'calling schedule func...'
	#url = 'http://simms-teach.com/cis90calendar.php'
	#calendar = scraper.calendar_page(url)
	interface.display_schedule()
	sys.exit(0)
else:
	print 'args:', sys.argv
	print 'calling grades funcs...'
	interface.display_user_summary(sys.argv[1])
	sys.exit(0)	
