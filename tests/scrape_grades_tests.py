import unittest
import requests
from bs4 import BeautifulSoup

from src.scraper import grades_ranges


class GradesPageTest(unittest.TestCase):

	def setUp(self):
		url = 'http://simms-teach.com/cis90grades.php'
		response = requests.get(url)
		soup = BeautifulSoup(response.text)
		table = soup.find('table', attrs={'class': 'grades'})
		self.rows = table.find_all('tr')[1:]  # ignore header row
	
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
