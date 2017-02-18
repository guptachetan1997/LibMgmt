import sqlite3

connection = sqlite3.connect('library.db')
cursor = connection.cursor()
cursor.execute('''PRAGMA foreign_keys=ON''')

class Librarian(object):
	def get(self, username):
		try:
			cursor.execute('''SELECT * FROM librarian WHERE username=:username''', (username, ))
			librarian = cursor.fetchone()
			self.librarianID = librarian[0]
			self.username = librarian[1]
			self.password = librarian[2]
			self.authenticated = False
			return self
		except Exception as e:
			print(e)
			return None

	def setup(self, username, password):
		self.username = username
		self.password = password

	def is_active(self):
		return True

	def get_id(self):
		return self.username

	def is_authenticated(self):
		return self.authenticated

	def is_anonymous(self):
		return False
