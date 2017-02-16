import sqlite3

connection = sqlite3.connect('library.db')
cursor = connection.cursor()
cursor.execute('''PRAGMA foreign_keys=ON''')

def create_tables():
	cursor.execute('''CREATE TABLE IF NOT EXISTS supplier (
	id	INTEGER PRIMARY KEY AUTOINCREMENT,
	name	TEXT NOT NULL,
	phone	TEXT NOT NULL,
	address	TEXT);''')
	connection.commit()
	print("Supplier Table Created")


	cursor.execute('''CREATE TABLE IF NOT EXISTS book(
	id	INTEGER PRIMARY KEY AUTOINCREMENT,
	title	VARCHAR(50) NOT NULL,
	author	VARCHAR(50) NOT NULL,
	publishDate DATE,
	publisher VARCHAR(50),
	isbn13 VARCHAR(13) UNIQUE,
	supplierID INTEGER,
	FOREIGN KEY (supplierID) references supplier (id));''')
	connection.commit()
	print("Book Table created")

	cursor.execute('''CREATE TABLE IF NOT EXISTS patron(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	cardNum INTEGER UNIQUE,
	name VARCHAR(50),
	age INTEGER,
	doj DATE,
	address TEXT,
	phone VARCHAR(10),
	borrowLimit INTEGER DEFAULT 2);''')
	connection.commit()
	print("User Table Created")

	cursor.execute('''CREATE TABLE IF NOT EXISTS issue(
	transID INTEGER PRIMARY KEY AUTOINCREMENT,
	bookID INTEGER,
	patronID INTEGER,
	issueDate DATE,
	FOREIGN KEY (bookID) REFERENCES book(id),
	FOREIGN KEY (patronID) REFERENCES patron(id));''')
	print("Issue Table Created")
	connection.commit()

	cursor.execute('''CREATE TABLE IF NOT EXISTS issue_history(
	transID INTEGER PRIMARY KEY,
	bookID INTEGER,
	patronID INTEGER,
	issueDate DATE,
	returnDate DATE,
	lateFees INTEGER,
	FOREIGN KEY (bookID) REFERENCES book(id),
	FOREIGN KEY (patronID) REFERENCES patron(id));''')
	print("Issue History Table Created")
	connection.commit()


if __name__ == '__main__':
	create_tables()