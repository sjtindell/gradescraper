from bs4 import BeautifulSoup
import requests
import time


URL = 'http://simms-teach.com/cis90calendar.php'


def calendar_page(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text)
	# [1:] ignore header row
	table_rows = soup.find_all('tr')[1:]
	return table_rows
