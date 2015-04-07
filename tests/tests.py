import src
import unittest


class CalendarPageTest(unittest.TestCase):
	# is the site up
	# is the calendar page there
	# are the column headers correct
	# do values in columns match expected
	pass


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
