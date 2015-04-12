import time

import requests
from bs4 import BeautifulSoup

import formatter
from point_values import point_values


def display_schedule(one_week=False):
	today = time.strftime("%m/%d")
	for row in formatter.calendar:
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
	user_points_row = formatter.get_user_row(name)
	user_total = sum(int(num) for num 
		in user_points_row[2:] if num != '*')
	possible = formatter.grades_page_possible_points()
	grade = round(float(user_total) / float(possible), 2) * 100
	
	print 'name:', name
	print 'have:', user_total, 'points'
	print 'possible:', possible
	print 'grade:', str(grade) + '%'


def display_user_scores(name):
	row = formatter.get_user_row(name)
	assignment_data = formatter.grades_page_current_assignments(name)
	for string, num, scores, worth in assignment_data:
		print
		for i in range(num):
			print '{0}{1}:'.format(string, num), scores[i], 'out of', worth, 'points'
	print 'Extra Credit:', row[30], 'out of 90'


def display_user_points_until(name):
	
	ranges = formatter.ranges
	user_points = formatter.get_user_row(name)
	
	user_total = sum(int(num) for num 
		in user_points[2:] if num != '*')
	points = user_total	

	if points >503:
		print "You've got an A...good job!"
	elif points in ranges['B']:
		#print "a B...too lazy to study, too smart to fail"
		print "You need", 504 - points, "points for an A"
	elif points in ranges['C']:
		#print "C's get degrees...but you only need"
		print 448 - points, "points for a B"
		print "and only", 504 - points, "points for an A"
	else:
		print "Only", 392 - points, "points to get a C and pass"
		print 448 - points, "points to get a B"
		print 504 - points, "points to get an A...you got this!"
	

def display_remaining_points():
	pass

