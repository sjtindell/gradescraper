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
		

class GradesPageUsersTableTest(unittest.TestCase):
	
	def setUp(self):
		self.url = 'http://simms-teach.com/cis90grades.php'
		self.response = requests.get(self.url)
		self.soup = BeautifulSoup(self.response.text)
		self.table = self.soup.find_all('table', attrs={'class': 'grades'})

	def header_row_cells(self, row):
		cells = row.find_all('td')
		cells = [str(cell).strip('</td>') for cell in cells]
		return cells
		
	def test_page_has_expected_header(self):
		self.assertEqual(self.soup.h2.text, 'CIS 90 Grades')

	def test_table_has_expected_header(self):
		headers = self.soup.find_all('h4')
		assert 'Current Progress' in [header.text for header in headers]

	def test_table_search_finds_multiple_tables(self):	
		self.assertEqual(len(self.table), 2)
	
	def test_number_of_table_headers(self):
		row = self.table[1].find_all('tr')[0]
		cells = self.header_row_cells(row)
		self.assertEqual(len(cells), 9)

	def test_table_header_strings(self):	
		row = self.table[1].find_all('tr')[0]
		cells = self.header_row_cells(row)

		expected_strings = (
			'Code', 'Grading', 'Quizzes',
			'Forum', 'Labs', 'Projec',  # correct for </td> stripping t 
			'Extra', 'Total', 'Grade'
		)

		for string, cell in zip(expected_strings, cells):
			assert string in cell

	def test_number_of_assignment_columns(self):
		row = self.table[1].find_all('tr')[1]
		cells = self.header_row_cells(row)
		all_cells_string = ''.join(cells)
		for test_string in ('Q1', 'Q10', 'L1', 'L10',
							'T1', 'T3', 'F1', 'F4'):
			assert test_string in all_cells_string	

	def test_table_max_points_total(self):	
		row = self.table[1].find_all('tr')[2]
		cells = self.header_row_cells(row)
		self.assertEqual(int(cells[-1]), 560)

