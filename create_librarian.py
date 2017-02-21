import sqlite3
import getpass
from flask_bcrypt import Bcrypt

connection = sqlite3.connect('library.db')
cursor = connection.cursor()
cursor.execute('''PRAGMA foreign_keys=ON''')
bcrypt = Bcrypt()

def addLibrarian():
	username = input("Username(Case Sensitive) : ")
	password1 = getpass.getpass()
	password2 = getpass.getpass()
	if password1 == password2:
		pass_hash = bcrypt.generate_password_hash(password1)
		try:
			cursor.execute('''
				INSERT INTO librarian(username,password)
				VALUES(?,?)
				''', (username, pass_hash))
			connection.commit()
			print("Success")
		except Exception as e:
			print("Failure")
	else:
		print("Passwords do not match.")

if __name__ == '__main__':
	addLibrarian()