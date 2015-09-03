import unittest
import requests
from bs4 import BeautifulSoup

from lib.scraper import GradesPage
from lib.point_values import point_values
from lib.formatter import UserData

class UserDataAPITest(unittest.TestCase):
	
	def setUp(self):
		self.page = GradesPage()
		self.user_rows = self.page.grade_rows_table
		self.ranges = self.page.grade_ranges_table
		self.forum_scores = self.page.forum_scores
		self.data = UserData('legolas')

	def test_user_row_formats_forum_score_into_correct_row(self):	
		expected_forum_string = self.user_rows[1]
		expected_char = 'F'
		self.assertEqual(expected_forum_string[15][0], expected_char)
		
	def test_check_columns_returns_None_for_first_rows(self):
		# early in semester, check some columns are empty
		# we start at column 3 because names and the word grade
		# take the first two
		columns = self.data.check_columns(2, 4)
		self.assertEqual(columns, 0)

	def test_check_columns_returns_some_for_more_assigns(self):
		# later in semester, check some columns are found
		columns = self.data.check_columns(0, 15)
		self.assertTrue(columns > 0)

	def test_possible_points_not_too_high(self):
		self.assertFalse(self.data.possible_points > 560)
