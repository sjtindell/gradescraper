from bs4 import BeautifulSoup
import os
import requests
import time


class CalendarPage(object):
	'''Scrape and organize the Calendar web page.'''

	def __init__(self):
		self.url = 'http://simms-teach.com/cis90calendar.php'
		self.response = requests.get(self.url)
		self.soup = BeautifulSoup(self.response.text, 'html.parser')  # needs html 5 parser specification on centos/py 2.6
		self.table_rows = self.soup.find_all('tr')[1:]
	
	@property  # decorator allows calling by simple name
	def calendar(self):
		rows_list = []
		for row in self.table_rows:
			entries = row.find_all('td')  # table data
	
			# calls the other methods from this class,
			# split for organization	
			row_data = {
				'lesson': self.row_lesson(entries),
				'date': self.row_date(entries),
				'activity': self.row_activity(entries),
				'due': self.row_due(entries)
			}
		
			rows_list.append(row_data)	
		return rows_list

	def row_lesson(self, entries):
		# unicode -> ascii ignore '\xa0'
		lesson = entries[0].string.encode('ascii', 'ignore')
		return lesson
	
	def row_date(self, entries):
		date = entries[1].string.replace('<td>', '').encode('ascii', 'ignore')
		date = time.strptime(date, '%m/%d')  # format since site returns dates 1/28 etc.
		date = time.strftime('%m/%d', date)  # python only does zero padded dates
		return date
		
	def row_activity(self, entries):
		topics = entries[2].h4
		if 'Quiz' in str(topics):
			activity = str(topics.a.text[:8])  # [:8] no extraneous text
		elif 'Test' in str(topics):
			activity = str(topics.text[:8])
		else:
			activity = ''
		return activity

	def row_due(self, entries):			
		due = [str(entry.text) for entry in entries[4].find_all('a')]
		return due


class GradesPage(object):
	
	def __init__(self):
		self.url = 'http://simms-teach.com/cis90grades.php'
		self.response = requests.get(self.url)
		self.soup = BeautifulSoup(self.response.text, 'html.parser')

	# author Rich Simms 2014
	# function to scrape private forum
	# scores from files in each specific
	# user's home directory
	@property
	def forum_scores(self):
		forum_file_names = ['f1.graded', 'f2.graded',
			'f3.graded', 'f4.graded']
		forum_scores = []

		for forum_file_name in forum_file_names:
			pts = 0
			home_dir = "/" + os.environ["LOGNAME"].replace("90", "") + "/"
			# for opus /home/cis90/
			# for test home/cis90
			file_name = "/home/cis90" + home_dir + forum_file_name
			
			try:
				with open(file_name, 'r') as f:
					line = f.readline()
					pts = int(line)
					forum_scores.append(pts)
			except IOError:
				continue
		return forum_scores

	# different ranges for an A, B, C, etc.
	@property
	def grade_ranges_table(self):
		table = self.soup.find('table', attrs={'class': 'grades'})
		rows = table.find_all('tr')[1:]  # ignore header row

		range_limit = []
		for row in rows:
			row = str(row).split('<td>')
			range_string = row[2].strip('</td>').split()
			low_grade = range_string[0]
			range_limit.append(int(low_grade))

		grades_ranges = {
			'B': range(range_limit[1], range_limit[0]),
			'C': range(range_limit[2], range_limit[1] -1),
			}
			
		return grades_ranges	

	@property
	def grade_rows_table(self):	
		student_rows = [ ]
		table = self.soup.find_all('table', attrs={'class': 'grades'})[1]
		for row in table.find_all('tr'):
			cells = row.find_all('td')
			cells = [str(cell).strip('</td>') for cell in cells]
			cells = [0 if cell == '\xc2\xa0' else cell for cell in cells]
			student_rows.append(cells)
		return student_rows
	


