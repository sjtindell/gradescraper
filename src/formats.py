import time

from scraper import calendar_page


def calendar_dict(table_rows):

	page_data = {}	

	for row in table_rows:
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

