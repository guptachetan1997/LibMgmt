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
	dob DATE,
	doj DATE,
	address TEXT,
	phone VARCHAR(10),
	borrowLimit INTEGER DEFAULT 2);''')
	connection.commit()
	print("User Table Created")

	cursor.execute('''CREATE TABLE IF NOT EXISTS patron_reg(
	regID INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50),
	dob DATE,
	address TEXT,
	phone VARCHAR(10));''')
	connection.commit()
	print("User Reg Table Created")

	cursor.execute('''CREATE TABLE IF NOT EXISTS issue(
	transID INTEGER PRIMARY KEY AUTOINCREMENT,
	bookID INTEGER,
	patronID INTEGER,
	librarianID INTEGER,
	issueDate DATE,
	FOREIGN KEY (bookID) REFERENCES book(id),
	FOREIGN KEY (patronID) REFERENCES patron(id),
	FOREIGN KEY (librarianID) REFERENCES librarian(id));''')
	print("Issue Table Created")
	connection.commit()

	cursor.execute('''CREATE TABLE IF NOT EXISTS issue_history(
	transID INTEGER PRIMARY KEY,
	bookID INTEGER,
	patronID INTEGER,
	issuedbyID INTEGER,
	returnedtoID INTEGER,
	issueDate DATE,
	returnDate DATE,
	lateFees INTEGER,
	FOREIGN KEY (bookID) REFERENCES book(id),
	FOREIGN KEY (patronID) REFERENCES patron(id),
	FOREIGN KEY (issuedbyID) REFERENCES librarian(id),
	FOREIGN KEY (returnedtoID) REFERENCES librarian(id));''')
	print("Issue History Table Created")
	connection.commit()

	cursor.execute('''CREATE TABLE IF NOT EXISTS librarian(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username VARCHAR(50) UNIQUE NOT NULL,  
	password VARCHAR(100) NOT NULL);''')
	connection.commit()
	print("Librarian table Created")


if __name__ == '__main__':
	create_tables()