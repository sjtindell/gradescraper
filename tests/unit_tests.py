from bs4 import BeautifulSoup
import re
import requests
import unittest

from src.scraper import scrape_calendar, get_calendar_data


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
		assert date_pattern.match(date_field)  # date

	
class ScrapeCalendarTest(unittest.TestCase):

	def setUp(self):
		self.url = 'http://simms-teach.com/cis90calendar.php'
		self.response = requests.get(self.url)
		self.soup = BeautifulSoup(self.response.text)
	
	def test_scrape_calendar_returns_table_rows(self):
		expected_rows = self.soup.find_all('tr')[1:]
		rows = scrape_calendar(self.url)
		assert rows == expected_rows
	
	
	# did we get all rows

	# is the dict layout as expected
	
	# are the dates as expected, spring vs fall
	# is the point total expected
	# are the dates handled right


if __name__ == '__main__':
	unittest.main()
