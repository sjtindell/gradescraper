import re
import sys
import time
import unittest

from lib.interface import display_schedule
from lib.point_values import point_values
from lib.scraper import CalendarPage



class NextWeekInterfaceTest(unittest.TestCase):

	def setUp(self):
		self.url = 'http://simms-teach.com/cis90calendar.php'
		self.calendar = CalendarPage().calendar
		self.today = time.strftime('%m/%d')
		
	def test_point_values_total(self):
		total = sum(point_values.values())
		self.assertEqual(total, 143)

	def test_assignment_names_in_calendar(self):
		# needs clean up
		all_class_work = []
		for row in self.calendar:
			all_class_work.extend(row['activity'].split())
			
			due = row['due']
			for string in due:
				for word in string.split():
					all_class_work.append(word)
		
		for name in point_values.keys():
			assert name in all_class_work

	def test_correct_difference_in_days(self):
		for row in self.calendar:
			date = row['date']
			if date > self.today:
				days = int(date[3:]) - int(self.today[3:])
				self.assertFalse(days > 7)
				break

	def test_due_in_string_in_output(self):
		display_schedule(one_week=True)
		output = sys.stdout.getvalue().strip()
		assert 'due in' in output

	def test_date_string_in_output(self):
		display_schedule(one_week=True)
		output = sys.stdout.getvalue().strip()
		pattern = re.compile(r'^[0-9]+[/][0-9]+$')
		line_one = output[:21]
		possible_date = line_one.split()[4]
		self.assertTrue(pattern.match(possible_date))

class RemainingWeeksInterfaceTest(unittest.TestCase):

	def setUp(self):
		self.url = 'http://simms-teach.com/cis90calendar.php'
		self.calendar = CalendarPage().calendar
		self.today = time.strftime('%m/%d')
	
	def test_calendar_date_difference(self):
		for row in self.calendar:
			date = row['date']
			diff = 0
			if date > self.today:
				if date[:2] == self.today[:2]:
					diff = int(date[3:]) - int(self.today[3:])
				elif date[:2] > self.today[:2]:
					diff = int(date[3:]) - int(self.today[3:]) + 30
			self.assertFalse(diff > 180)

	def test_simple_strings_in_output(self):
		display_schedule()
		output = sys.stdout.getvalue().strip()
		print output
		assert 'due in' in output
		assert 'worth' in output

	def test_output_days_left_in_ascending_order(self):
		display_schedule()
		output = sys.stdout.getvalue().strip()
		previous = 0
		for line in output:
			if 'due in' in line:
				line = line.split()
				days_left = int(line[2])
				self.assertTrue(days_left > previous)
				previous = days_left
	
	def test_date_string_in_output(self):
		display_schedule()
		output = sys.stdout.getvalue().strip()
		pattern = re.compile(r'^[0-9]+[/][0-9]+$')
		line_one = output[:21]
		possible_date = line_one.split()[4]
		self.assertTrue(pattern.match(possible_date))

	def test_output_dates_in_ascending_order(self):
		display_schedule()
		output = sys.stdout.getvalue().strip()
		previous_date = ''
		for line in output:
			if 'due in' in line:
				line = line.split()
				date = line[4]	
				self.assertTrue(date > previous_date)
				previous_date = date
	
	def test_assignment_names_in_output(self):
		# often fails, fragile test
		display_schedule()
		output = sys.stdout.getvalue().strip()	
		for assignment_name in point_values.keys():
			assert assignment_name in output
