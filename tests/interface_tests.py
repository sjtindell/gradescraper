import sys
import time
import unittest

from src.interface import display_next_week, display_remaining_weeks
from src.point_values import point_values
from src.scraper import calendar_page



class ScheduleInterfaceTest(unittest.TestCase):

	def setUp(self):
		self.url = 'http://simms-teach.com/cis90calendar.php'
		self.calendar = calendar_page(self.url)
		self.today = time.strftime('%m/%d')
		
	def test_point_values_total(self):
		total = sum(point_values.values())
		self.assertEqual(total, 203)

	def test_assignment_names_in_calendar(self):
		# needs clean up
		all_class_work = []
		for row in self.calendar:
			all_class_work.extend(row['activity'].split())
			
			due = row['due']
			for string in due:
				for word in string.split():
					all_class_work.append(word)

		print all_class_work
		for name in point_values.keys():
			assert name in all_class_work

	def test_correct_difference_in_days(self):
		for row in self.calendar:
			date = row['date']
			if date > self.today:
				days = int(date[3:]) - int(self.today[3:])
				self.assertFalse(days > 7)
				break

	def test_disp_next_week_output(self):
		display_next_week()
		output = sys.stdout.getvalue().strip()
		assert 'due in' in output
		assert 'worth' in output
		


