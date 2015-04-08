from bs4 import BeautifulSoup
import requests
import time


# for testing
url = 'http://simms-teach.com/cis90calendar.php'


def calendar_page(url):
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
		elif date == '1/28':
			activity = 'First Day'
		elif date == '2/7':
			activity = 'Last Day to Add CIS90'
		elif date == '4/1':
			activity = 'Spring Break'
		else:
			activity = 'None'

		due = [str(entry.text) for entry in entries[4].find_all('a')]
		
		# blank string, list = 'None' 
		# for visual organization.
		# dates always present.

		page_data = {
			'lesson': lesson,
			'date': date,
			'activity': activity,
			'due': due
		}
	
		rows_list.append(page_data)
	
	return rows_list

