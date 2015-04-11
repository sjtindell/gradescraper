import sys
import time
import unittest

from src.interface import display_schedule
from src.point_values import point_values
from src.scraper import calendar_page



class NextWeekInterfaceTest(unittest.TestCase):

	def setUp(self):
		self.url = 'http://simms-teach.com/cis90calendar.php'
		self.calendar = calendar_page(self.url)
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

	def test_correct_strings_in_output(self):
		display_schedule(one_week=True)
		output = sys.stdout.getvalue().strip()
		assert 'due in' in output
		assert 'worth' in output
		

class RemainingWeeksInterfaceTest(unittest.TestCase):

	def setUp(self):
		self.url = 'http://simms-teach.com/cis90calendar.php'
		self.calendar = calendar_page(self.url)
		self.today = time.strftime('%m/%d')

	def test_date_difference_not_too_big(self):
		for row in self.calendar:
			date = row['date']
			diff = 0
			if date > self.today:
				if date[:2] == self.today[:2]:
					diff = int(date[3:]) - int(self.today[3:])
				elif date[:2] > self.today[:2]:
					diff = int(date[3:]) - int(self.today[3:]) + 30
			self.assertFalse(diff > 180)

	def test_correct_strings_in_output(self):
		display_schedule()
		output = sys.stdout.getvalue().strip()
		assert 'due in' in output
		assert 'worth' in output

			
	
