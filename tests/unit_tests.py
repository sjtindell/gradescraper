from bs4 import BeautifulSoup
import re
import requests
import time
import unittest

from src.scraper import scrape_calendar, format_calendar_data


class CalendarPageTest(unittest.TestCase):

	def setUp(self):
		self.url = 'http://simms-teach.com/cis90calendar.php'
		self.response = requests.get(self.url)
		self.soup = BeautifulSoup(self.response.text)
	
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
		self.url = 'http://simms-teach.com/cis90calendar.php'
		# scraper.py.get_calenda_data
		# returns dict {lesson: {date:v, in_class:v, due:v, }	
		self.calendar = format_calendar_data(self.url)
	
	def test_scrape_calendar_method_returns_table_rows(self):
		response = requests.get(self.url)
		soup = BeautifulSoup(response.text)
		expected_rows = soup.find_all('tr')[1:]

		rows = scrape_calendar(self.url)

		assert rows == expected_rows
		assert len(rows) is 18
		
	# {lesson # {class date, activities in class, due today}}
	def test_check_schedule_dict_lessons_int_range(self):	
		site_range = (int(key) for key in self.calendar.keys() if key)
		assert sum(site_range) is sum(range(1, 16))

	def test_check_schedule_dict_dates_format(self):
		date_pattern = re.compile('^[0-9]+[/][0-9]+$')
		for value in self.calendar.values():
			assert date_pattern.match(value['date'])

	def test_check_schedule_dict_number_of_activities(self):
		quizzes, tests = 0, 0
		for value in self.calendar.values():
			assignment = value['activity']
			if 'Quiz' in assignment:
				quizzes += 1
			elif 'Test' in assignment:
				tests += 1
		assert quizzes is 10
		assert tests is 3
				
		# due today
		# right number of labs, forums
	def test_check_schedule_dict_number_of_labs_and_forums(self):
		check_strings = {
			'Lab': 0, 
			'posts': 0, 
			'Project': 0, 
			'Survey': 0, 
			'X1': 0, 
			'X2': 0
		}
		
		for assignment_list in self.calendar.values():
			for assign in assignment_list['due']:
				for string in check_strings.keys():
					if string in assign:
							check_strings[string] += 1
			
		expected = (12, 4, 1, 1, 1, 1)
		assert sum(expected) is sum(check_strings.values())
			
	def test_correct_dates_for_spring_and_fall(self):
		today = time.strftime("%m/%d")
		for value in self.calendar.values():
			date = time.strptime(value['date'], "%m/%d")
			date = time.strftime("%m/%d", date)
			if today < "09/01":
				assert date < "09/01"
			elif today > "09/01":
				assert date > "09/01"
