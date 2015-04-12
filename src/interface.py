import time

import requests
from bs4 import BeautifulSoup

import formatter
import scraper
from point_values import point_values


def display_schedule(one_week=False):
	today = time.strftime("%m/%d")
	url = 'http://simms-teach.com/cis90calendar.php'
	calendar = scraper.calendar_page(url)
	for row in calendar:
		date = row['date']
		if date > today:	
			if date[:2] == today[:2]:
				diff = int(date[3:]) - int(today[3:])
			elif date[:2] > today[:2]:
				diff = int(date[3:]) - int(today[3:]) + 30
			print
			print 'due in', diff, 'days:', date
			
			for name, value in point_values.items():
				for assignment in row['due']:
					if name in assignment:
						print assignment, 'worth', value, 'points'
				
				if name in row['activity']:
					print row['activity'], 'worth', value, 'points'
			if one_week:
				break

	
def display_user_summary(name):
	user_points = formatter.get_user_row(name)
	user_total = sum(int(num) for num 
		in user_points[2:] if num != '*')
	
	print 'name:', name
	print 'have:', user_total, 'points'
	print 'possible:', formatter.grades_page_possible_points()


def display_user_scores():
	pass

def display_user_points_until():
	pass

def display_remaining_points():
	pass

