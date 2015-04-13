from scraper import GradesPage
from point_values import point_values


class UserData(object):
	
	def __init__(self, name):
		self.name = name
		with GradesPage() as page:
			self.user_rows = page.grade_rows_table[3:]
			self.ranges = page.grade_ranges_table
			self.forum_scores = page.forum_scores

	@property
	def user_row(self):
		for row in self.user_rows:
			if self.name == row[0]:
				start = 15
				stop = start + len(self.forum_scores)
				row[start: stop] = self.forum_scores
				return row

	def check_columns(self, start, stop):	
		count = 0
		while start < stop:
			try:
				test = all(row[start] == 0 for row in self.user_rows)
				if test:
					return count
				count += 1
				start += 1
			except IndexError:
				return count

	def completed_assignments(self):
		return (
		self.check_columns(2, 12),
		self.check_columns(12, 15),
		self.check_columns(15, 19),
		self.check_columns(19, 29),
		self.check_columns(29, 30)
		)

	@property
	def possible_points(self):
		quizzes, tests, forums, labs, project = self.completed_assignments()

		return int(
			point_values['Quiz'] * quizzes +
			point_values['Test'] * tests +
			point_values['posts'] * forums +
			point_values['Lab'] * labs +
			point_values['Project'] * project)

	@property	
	def current_assignments(self):
		assignment_strings = (
			'Quiz', 'Test', 'Forum', 
			'Lab', 'Project'
		)
		assignment_worth = (3, 30, 20, 30, 60)
		assignment_nums = self.completed_assignments()
		
		row = self.user_row
		
		user_scores = [
			row[2:12], row[12:15], row[15: 19],
			row[19: 29], row[29: 30]
		]

		combined_data = zip(assignment_strings, assignment_nums,
			user_scores, assignment_worth)
		
		return combined_data	

	def __enter__(self):
		return self
	
	def __exit__(self, sysin, sysout, syserr):
		pass

