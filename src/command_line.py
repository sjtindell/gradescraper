# take args, display views
# def display_see_more():
#	pass

# for testing
import sys
import interface


if sys.argv[1] == 'schedule':
	print 'args:', sys.argv
	print 'calling schedule func...'
	interface.display_schedule()		
