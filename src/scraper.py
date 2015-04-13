import os
import time

from bs4 import BeautifulSoup
import requests


# for testing
urls = ('http://simms-teach.com/cis90calendar.php',
		'http://simms-teach.com/cis90grades.php')


def calendar_page(url):
	''' Returns a list in which each item is 
	a dictionary of values from a row in the calendar.'''
	response = requests.get(url)
	soup = BeautifulSoup(response.text)

	# table_rows, [1:] ignore headers
	table_rows = soup.find_all('tr')[1:]
	
	# a list of dicts because order will
	# matter for dates, assigns
	rows_list = []

	for row in table_rows:
		entries = row.find_all('td')  # table data

		# unicode -> ascii ignore '\xa0'
		lesson = entries[0].string.encode('ascii', 'ignore')

		date = entries[1].string.replace('<td>', '').encode('ascii', 'ignore')
		date = time.strptime(date, '%m/%d')  # site returns dates 1/28 etc.
		date = time.strftime('%m/%d', date)  # python only does zero padded dates

		# get activity from topics
		# site uses various tags, locations
		# so If statements to handle
		topics = entries[2].h4
		if 'Quiz' in str(topics):
			activity = str(topics.a.text[:8])  # [:8] no extraneous text
		elif 'Test' in str(topics):
			activity = str(topics.text[:8])
		else:
			activity = ''

		due = [str(entry.text) for entry in entries[4].find_all('a')]
		
		# blank string, list = 'None' 
		# for visual organization.
		# dates always present.

		row_data = {
			'lesson': lesson,
			'date': date,
			'activity': activity,
			'due': due
		}
	
		rows_list.append(row_data)
	
	return rows_list


def grades_page_ranges(html_soup):
	# grades table contains grades ranges
	table = html_soup.find('table', attrs={'class': 'grades'})
	rows = table.find_all('tr')[1:]  # ignore header row

	range_limit = []
	for row in rows:
		# ranges are table data ints
		row = str(row).split('<td>')
		range_string = row[2].strip('</td>').split()
		low_grade = range_string[0]
		range_limit.append(int(low_grade))

	# can add further ranges in future
	grades_ranges = {
		'B': range(range_limit[1], range_limit[0]),
		'C': range(range_limit[2], range_limit[1] -1),
		}
		
	return grades_ranges		

def grades_ranges(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text)
	return grades_page_ranges(soup)


def grades_page_user_rows(html_soup):
	student_rows = [ ]
	table = html_soup.find_all('table', attrs={'class': 'grades'})[1]
	for row in table.find_all('tr'):
		cells = row.find_all('td')
		cells = [str(cell).strip('</td>') for cell in cells]
		cells = [0 if cell == '\xc2\xa0' else cell for cell in cells]
		student_rows.append(cells)
	return student_rows

def grades_table(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text)
	return grades_page_user_rows(soup)


def forum_scores():
	forum_file_names = ['f1.graded', 'f2.graded',
				  'f3.graded', 'f4.graded']
	forum_scores = []

	for forum_file_name in forum_file_names:
		pts = 0
		home_dir = "/" + os.environ["LOGNAME"].replace("90", "") + "/"
		# for opus /home/cis90/
		file_name = "/home/cis90" + home_dir + forum_file_name
		
		try:
			with open(file_name, 'r') as f:
				line = f.readline()
				pts = int(line)
				forum_scores.append(pts)
		except IOError:
			continue
	return forum_scores

