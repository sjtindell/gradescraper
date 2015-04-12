import unittest
import requests
from bs4 import BeautifulSoup

from src.scraper import grades_page_ranges, grades_page_user_rows


class ScrapeGradesPageRangesTest(unittest.TestCase):

	def setUp(self):
		self.url = 'http://simms-teach.com/cis90grades.php'
		self.response = requests.get(self.url)
		self.soup = BeautifulSoup(self.response.text)
		self.table = self.soup.find('table', attrs={'class': 'grades'})
		self.rows = self.table.find_all('tr')[1:]  # ignore header row
	
	def test_range_table_row_one_strings(self):
		for string in ('higher', 'A', 'Pass'):
			assert string in str(self.rows[0])

	def test_range_table_number_of_rows(self):
		self.assertEqual(len(self.rows), 5)

	def test_range_table_start_column_ints(self):
		expected_ints = (504, 448, 392, 336, 0)
		i = 0 

		for row in self.rows:
			# ranges are table data ints
			row = str(row).split('<td>')
			range_string = row[2].strip('</td>').split()
			low_grade = int(range_string[0])
			self.assertEqual(low_grade, expected_ints[i])
			i += 1

	def test_scrape_ranges_returns_grades_as_keys(self):
		ranges = grades_page_ranges(self.soup)
		for grade in ('B', 'C'):
			assert grade in ranges.keys()

	def test_scrape_ranges_returns_lists_of_ints_as_values(self):	
		ranges = grades_page_ranges(self.soup)
		assert type(ranges) is dict
		assert type(ranges.values()[0]) is list

	def test_scrape_range_returns_correct_range(self):
		ranges = grades_page_ranges(self.soup)
		tmp = [ ]
		for row in self.rows:
			row = str(row).split('<td>')
			range_string = row[2].strip('</td>').split()
			low_grade = int(range_string[0])
			tmp.append(low_grade)

		expected_range = range(tmp[1], tmp[0])
		self.assertEqual(ranges['B'], expected_range)
		

class ScrapeGradesPageUserRowsTest(unittest.TestCase):
	pass
