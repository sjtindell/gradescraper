import scraper
from point_values import point_values


url = 'http://simms-teach.com/cis90grades.php'
user_rows = scraper.grades_page(url)[3:]


def get_user_row(name):
	for user in user_rows:
		if name == user[0]:
			return user

def check_columns(start, stop):
	
	count = 0

	while start < stop:
		try:
			test = all(row[start] == 0 for row in user_rows)
			if test:
				return count
			count += 1
			start += 1
		except IndexError:
			print 'index error'
			return count


def grades_page_possible_points():
	quizzes = check_columns(2, 12)
	tests = check_columns(12, 15)
	forums = check_columns(15, 19)
	labs = check_columns(19, 29)
	project = check_columns(29, 30)

	return int(
		point_values['Quiz'] * quizzes +
		point_values['Test'] * tests +
		point_values['posts'] * forums +
		point_values['Lab'] * labs +
		point_values['Project'] * project)

