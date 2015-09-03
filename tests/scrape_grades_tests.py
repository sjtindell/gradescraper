import re
import unittest

import requests
from bs4 import BeautifulSoup

from lib.scraper import GradesPage


class ScrapeGradesPageRangesTest(unittest.TestCase):

	def setUp(self):
		self.url = 'http://simms-teach.com/cis90grades.php'
		self.response = requests.get(self.url)
		self.soup = BeautifulSoup(self.response.text, 'html.parser')
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
		page = GradesPage()
		ranges = page.grade_ranges_table
		for grade in ('B', 'C'):
			assert grade in ranges.keys()

	def test_scrape_ranges_returns_lists_of_ints_as_values(self):	
		page = GradesPage()
		ranges = page.grade_ranges_table
		assert type(ranges) is dict
		assert type(ranges.values()[0]) is list

	def test_scrape_range_returns_correct_range(self):
		page = GradesPage()
		ranges = page.grade_ranges_table
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
		self.soup = BeautifulSoup(self.response.text, 'html.parser')
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
		# excluding project, extra credit, total
		# expects just Q1-10, L1-10, etc.
		row = self.table[1].find_all('tr')[1]
		cells = self.header_row_cells(row)
		self.assertEqual(len(cells), 27)
	
	def test_assignment_column_strings(self):
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

	def test_table_user_row_format(self):
		# fails early in semester when there is nothing in the table	
		row = self.table[1].find_all('tr')[3]
		cells = self.header_row_cells(row)
		cells = [str(cell).strip('</td>') for cell in cells]
		cells = [str(0) if cell == '\xc2\xa0' else cell for cell in cells]
		all_cells_string = ''.join(cells)
		row_pattern = re.compile('^[a-z]+[0-9]+[*]+[0-9]+$')
		self.assertTrue(row_pattern.match(all_cells_string))
	

class GradesPageUserRowsFuncTest(unittest.TestCase):
		
		def setUp(self):
			self.url = 'http://simms-teach.com/cis90grades.php'
			self.response = requests.get(self.url)
			self.soup = BeautifulSoup(self.response.text, 'html.parser')
			self.my_table = GradesPage().grade_rows_table
		
		def test_return_table_row_format(self):
			returned_row = [str(score) for score in self.my_table[3]]
			all_cells_string = ''.join(returned_row)
			row_pattern = re.compile('^[a-z]+[0-9]+[*]+[0-9]+$')
			self.assertTrue(row_pattern.match(all_cells_string))

		def test_return_table_row_length(self):
			returned_row = [str(score) for score in self.my_table[3]]
			#name,gradingchoice, Q1-10, T1-3, F1-4, L1-10, Proj, EC, T, G
			self.assertEqual(len(returned_row), 33)	

		def test_return_a_few_lotr_names(self):
			returned_row = [str(score) for row in self.my_table for score in row]
			assert 'boromir' in returned_row
			assert 'strider' in returned_row
			assert 'frodo' in returned_row

		def test_returned_scores_seem_appropriate(self):
			user_row = self.my_table[5]
			# expected assignment values: quiz, test, lab
			self.assertTrue(int(user_row[5]) < 5)
			self.assertTrue(int(user_row[12]) < 35)
			self.assertTrue(int(user_row[24]) < 32)


