from bs4 import BeautifulSoup
import re
import requests
import unittest


class CalendarPageTest(unittest.TestCase):
	
	# is the site up
	url = 'http://simms-teach.com/cis90calendar.php'
	response = requests.get(url)
	assert response.status_code is 200
	
	# Is Cis 90 Calendar present
	soup = BeautifulSoup(response.text)
	assert 'CIS 90 Calendar' in soup.h2
	
	# are the column headers correct
	expected_headers = ('Lesson', 'Date', 'Topics',
						'Chapter', 'Due*')
	table_headers = soup.find_all('th')
	pairs = zip(expected_headers, table_headers)
	assert all(eh in th for eh, th in pairs)

	# do values in columns match expected
	table_row = soup.find_all('tr')[1]
	table_data = table_row.find_all('td')

	# two columns present satisfactory for now
	lesson_field = table_data[0].string
	assert int(lesson_field)
	date_field = table_data[1].string
	date_pattern = re.compile('^[0-9]+[/][0-9]+$')
	assert date_pattern.match(date_field)  # date

	
class ScrapeCalendarTest(unittest.TestCase):
	# from scraped data
	# is the number of assignments expected
	# is the point total expected
	# are the dates handled right
	pass


class BuildScheduleTest(unittest.TestCase):
	# does the proper data get stored
	# does the data stored match the website
	pass

class Test(unittest.TestCase):
	
	def setup(self):
		print('setup!')

	def teardown(self):
		print('tear down!')

	def test_basic(self):
		print('i ran!')


if __name__ == '__main__':
	unittest.main()
