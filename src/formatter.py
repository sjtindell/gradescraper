import scraper
from point_values import point_values


url = 'http://simms-teach.com/cis90grades.php'
user_rows = scraper.grades_table(url)[3:]
ranges = scraper.grades_ranges(url)


cal_url = 'http://simms-teach.com/cis90calendar.php'
calendar = scraper.calendar_page(cal_url)


def get_user_row(name):
	for row in user_rows:
		if name == row[0]:
			forum_scores = scraper.forum_scores()
			start = 15
			stop = start + len(forum_scores)
			row[start: stop] = forum_scores
			return row


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
			return count


def completed_assignments():
	return (
	check_columns(2, 12),
	check_columns(12, 15),
	check_columns(15, 19),
	check_columns(19, 29),
	check_columns(29, 30)
	)

def grades_page_possible_points():
	quizzes, tests, forums, labs, project = completed_assignments()

	return int(
		point_values['Quiz'] * quizzes +
		point_values['Test'] * tests +
		point_values['posts'] * forums +
		point_values['Lab'] * labs +
		point_values['Project'] * project)

	
def grades_page_current_assignments(name):
	assignment_strings = (
		'Quiz', 'Test', 'Forum', 
		'Lab', 'Project'
	)
	assignment_worth = (3, 30, 20, 30, 60)
	assignment_nums = completed_assignments()
	
	row = get_user_row(name)
	
	user_scores = [
		row[2:12], row[12:15], row[15: 19],
		row[19: 29], row[29: 30]
	]

	combined_data = zip(assignment_strings, assignment_nums,
		user_scores, assignment_worth)
	
	return combined_data	

