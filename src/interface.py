import time

import scraper
from point_values import *  
# QUIZ, LAB, FORUMS, 
# TEST, PROJECT, X1, X2


def retrieve_data():
	url = 'http://simms-teach.com/cis90calendar.php'
	lessons = scraper.calendar_page(url)
	return lessons

def display_next_week():
	# due in x days: date
	# quiz {0} worth {1} points
	# lab {0} worth {1} points
	pass	
	
def display_remaining_weeks():
	pass


def display_user_summary():
	pass

def display_user_scores():
	pass

def display_user_points_until():
	pass

def display_remaining_points():
	pass

