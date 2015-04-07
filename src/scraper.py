from bs4 import BeautifulSoup
import requests
import time

def scrape_calendar(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text)
	# retrieve rows, ignore header row
	table_rows = soup.find_all('tr')[1:]
	return table_rows


def format_calendar_data(url):

	rows = scrape_calendar(url)

	page_data = {}	

	for row in rows:
		entries = row.find_all('td')

		lesson = entries[0].string.encode('ascii', 'ignore')
		date = str(entries[1].string.replace('<td>', ''))
		topics = entries[2].h4
		
		# [:8] to remove extraneous text
		if 'Quiz' in str(topics):
			activity = topics.a.text[:8]
		elif 'Test' in str(topics):
			activity = topics.text[:8]
		else:
			activity = ''

		due = (str(entry.text) for entry in entries[4].find_all('a'))
		
		page_data[lesson] = {
			'date': date,
			'activity': activity,
			'due': due
		}

	
	return page_data

format_calendar_data('http://simms-teach.com/cis90calendar.php')

