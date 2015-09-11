import time
from scraper import CalendarPage
from formatter import UserData
from point_values import point_values


def display_schedule(one_week=False):
	today = time.strftime("%m/%d")
	for row in CalendarPage().calendar:
		date = row['date']
		if date > today:	
			if date[:2] == today[:2]:
				diff = int(date[3:]) - int(today[3:])
			elif date[:2] > today[:2]:
				diff = int(date[3:]) - int(today[3:]) + 30
			print
			print 'due in', diff, 'days:', date
			
			for name, value in point_values.items():
                                if not row['due'] and not row['activity']:
                                        print 'nothing due this day'
                                        break

				for assignment in row['due']:
					if name in assignment:
						print assignment, 'worth', value, 'points'
				
				if name in row['activity']:
					print row['activity'], 'worth', value, 'points'
			if one_week:
				break
			else:
				print
	
def display_user_summary(data):
	user_total = sum(int(num) for num 
		in data.user_row[2:] if num != '*')
	# throws float division error if scores are both 0.0
	if float(user_total) == 0.0 and float(data.possible_points) == 0.0:
		grade = 100
	else:
		grade = round(float(user_total) / float(data.possible_points), 2) * 100
	
	print 'name:', data.name
	print 'have:', user_total, 'points'
	print 'possible:', data.possible_points
	print 'grade:', str(grade) + '%'


def display_user_scores(data):
	for string, num, scores, worth in data.current_assignments:
		nums = range(1, num + 1)
		print
		for i in range(num):
			print '{0}{1}:'.format(string, nums[i]), scores[i], 'out of', worth, 'points'
	print 'Extra Credit:', data.user_row[30], 'out of 90'


def display_user_points_until(data):
	points = sum(int(num) for num 
		in data.user_row[2:] if num != '*')

	if points >503:
		print "You've got an A...good job!"
	elif points in data.ranges['B']:
		#print "a B...too lazy to study, too smart to fail"
		print "You need", 504 - points, "points for an A"
	elif points in data.ranges['C']:
		#print "C's get degrees...but you only need"
		print 448 - points, "points for a B"
		print "and only", 504 - points, "points for an A"
	else:
		print "Only", 392 - points, "points to get a C and pass"
		print 448 - points, "points to get a B"
		print 504 - points, "points to get an A...you got this!"
	

def display_remaining_points(data):
	today = time.strftime("%m/%d")
	user_scores = data.user_row
	extra_credit = int(user_scores[30])
	total_points = [ ]
	for row in CalendarPage().calendar:
		date = row['date']
		if date > today:	
			if date[:2] == today[:2]:
				diff = int(date[3:]) - int(today[3:])
			elif date[:2] > today[:2]:
				diff = int(date[3:]) - int(today[3:]) + 30
			print
			print 'due in', diff, 'days:', date
			
			for name, value in point_values.items():
                                if not row['due'] and not row['activity']:
                                        print 'nothing due this day'
                                        break
				for assignment in row['due']:
					if name in assignment:
						print assignment, 'worth', value, 'points'
						total_points.append(value)	
				
				if name in row['activity']:
					print row['activity'], 'worth', value, 'points'
					total_points.append(value)
	print
	ec = 90 - extra_credit
	print 'Extra Credit Remaining:', ec
	print 'Total Remaining:', sum(total_points) - 60 + ec  # correct for lab x1, x2
	print
