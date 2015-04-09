import time

import scraper
from point_values import point_values


def retrieve_data():
	url = 'http://simms-teach.com/cis90calendar.php'
	return scraper.calendar_page(url)

def display_next_week():
	today = time.strftime("%m/%d")
	for row in retrieve_data():
		date = row['date']
		if date > today:
			days = int(date[3:]) - int(today[3:])
			print 'due in', days, 'days:', date
			
			for name, value in point_values.items():
				for assignment in row['due']:
					if name in assignment:
						print assignment, 'worth', value, 'points'
				
				if name in row['activity']:
					print row['activity'], 'worth', value, 'points'
			break
	# quiz {0} worth {1} points
	# lab {0} worth {1} points

display_next_week()
	
def display_remaining_weeks():
	pass


def display_user_summary():
	pass

def display_user_scores():
	pass

def display_user_points_until():
	pass

def display_remaining_points():
	pass

