import re
import time
import unittest

from bs4 import BeautifulSoup
import requests

from src.scraper import CalendarPage


class CalendarPageTest(unittest.TestCase):

	def setUp(self):
		self.url = 'http://simms-teach.com/cis90calendar.php'
		self.response = requests.get(self.url)
		self.soup = BeautifulSoup(self.response.text, 'html.parser')
	
	def test_site_is_up(self):
		assert self.response.status_code is 200
	
	def test_page_header_correct(self):
		assert 'CIS 90 Calendar' in self.soup.h2
	
	def test_column_headers_correct(self):
		expected_headers = ('Lesson', 'Date', 'Topics',
							'Chapter', 'Due*')
		table_headers = self.soup.find_all('th')
		pairs = zip(expected_headers, table_headers)
		assert all(eh in th for eh, th in pairs)

	def test_values_in_columns_match_expected_format(self):
		table_row = self.soup.find_all('tr')[1]
		table_data = table_row.find_all('td')

		# two columns present satisfactory for now
		lesson_field = table_data[0].string
		assert int(lesson_field)
		date_field = table_data[1].string
		date_pattern = re.compile('^[0-9]+[/][0-9]+$')
		assert date_pattern.match(date_field)  # datie


class ScrapeCalendarTest(unittest.TestCase):

	def setUp(self):
		self.today = time.strftime("%m/%d")
		self.url = 'http://simms-teach.com/cis90calendar.php'
		# scraper.py.get_calenda_data
		# returns dict {lesson: {date:v, in_class:v, due:v, }
		self.calendar = CalendarPage().calendar
	
	def test_calendar_page_returns_all_rows(self):
		response = requests.get(self.url)
		soup = BeautifulSoup(response.text, 'html.parser')
		expected_rows = soup.find_all('tr')[1:]
		returned_rows = self.calendar
		assert len(expected_rows) == len(returned_rows)
		
	def test_check_schedule_dict_lessons_int_range(self):	
		lesson_num_sum = 0
		for row_dict in self.calendar:
			if row_dict['lesson']:
				lesson_num_sum += int(row_dict['lesson'])
		assert lesson_num_sum == sum(range(1, 16))
		
	def test_check_schedule_dict_dates_format(self):
		date_pattern = re.compile('^[0-9]+[/][0-9]+$')
		for row in self.calendar:
			assert date_pattern.match(row['date'])

	def test_check_schedule_dict_number_of_activities(self):
		quizzes, tests = 0, 0
		for row in self.calendar:
			activity = row['activity']
			if 'Quiz' in activity:
				quizzes += 1
			elif 'Test' in activity:
				tests += 1
		assert quizzes is 10
		assert tests is 3
				
		# due today
		# right number of labs, forums
	def test_check_schedule_dict_number_of_assigments(self):
		check_strings = {
			'Lab': 0, 
			'posts': 0, 
			'Project': 0, 
			'Survey': 0, 
			'X1': 0, 
			'X2': 0
		}
		
		for row in self.calendar:
			for assignment in row['due']:
				for string in check_strings.keys():
					if string in assignment:
						check_strings[string] += 1

		expected = (12, 4, 1, 1, 1, 1)
		assert sum(check_strings.values()) == sum(expected)
			
	def test_correct_dates_for_spring_and_fall(self):
		for row in self.calendar:
			date = row['date']
			# spring starts jan so if fall
			# hasnt started yet we must be 1 - 9
			if self.today < "09/01":
				assert date < "09/01"
			# fall ends late december so if not spring
			# we must be range 9 - 12
			elif self.today > "09/01":
				assert date > "09/01"

	def test_during_spring_get_spring_dates(self):
		start, end =  "01/25", "05/25"
	
		if start < self.today < end:
			for row in self.calendar:
				self.assertTrue(start < row['date'] < end)
				
	
	def test_during_fall_get_fall_dates(self):
		start, end = "09/01", "12/25"
		
		if start < self.today < end:
			for row in self.calendar:
				self.assertTrue(start < row['date'] < end)





