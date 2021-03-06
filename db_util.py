import sqlite3

connection = sqlite3.connect('library.db')
cursor = connection.cursor()
cursor.execute('''PRAGMA foreign_keys=ON''')	

def insertSupplier(supplier):
	try:
		cursor.execute('''INSERT INTO supplier(name, phone, address) VALUES(:name,:phone,:address)''', supplier)
		connection.commit()
		return True
	except Exception as e:
		print(e)
		return False

def insertBook(book):
	try:
		cursor.execute(
		'''INSERT INTO book(title, author, publishDate, publisher, isbn13, supplierID) 
			VALUES(:title, :author, :publishDate, :publisher, :isbn13, :supplierID)''', book)
		connection.commit()
		return True
	except Exception as e:
		print(e)
		return False

def insertPatronReg(patron):
	try:
		cursor.execute('''
			INSERT INTO patron_reg(name, dob, address, phone)
			VALUES(:name, :dob, :address, :phone)
			''', patron)
		connection.commit()
		return True
	except Exception as e:
		print(e)
		return False

def queryPatronReg():
	try:
		cursor.execute('''SELECT * FROM patron_reg;''')
		regs = cursor.fetchall()
		return regs
	except Exception as e:
		print(e)
		return None

def querySinglePatronReg(regID):
	try:
		cursor.execute('''SELECT * FROM patron_reg WHERE regID=:regID;''', (regID,))
		reg = cursor.fetchone()
		return reg
	except Exception as e:
		print(e)
		return None

def deletePatronReg(regID):
	try:
		cursor.execute('''DELETE FROM patron_reg WHERE regID=:regID''', (regID,))
		connection.commit()
		return True
	except Exception as e:
		print(e)
		return False

def insertPatron(patron):
	try:
		cursor.execute(
		'''INSERT INTO patron(cardNum,name,dob,doj,address,phone,borrowLimit) 
		VALUES(:cardNum,:name,:dob,:doj,:address,:phone,:borrowLimit)''', patron)
		connection.commit()
		return True
	except Exception as e:
		print(e)
		return False

def getPatronIssues(patronID):
	try:
		cursor.execute(
			'''
			SELECT bookID,title,issueDate 
			FROM issue,book 
			WHERE bookID=book.id AND patronID=?;
			''', (patronID, ))
		issues = cursor.fetchall()
		return issues
	except Exception as e:
		print(e)
		return None

def isUniqueCardNumber(canumber):
	try:
		cursor.execute('''
			SELECT COUNT(*) FROM patron WHERE cardNum=?''', (canumber, ))
		num = cursor.fetchone()
		return num[0] == 0
	except Exception as e:
		print(e)
		return None

def insertIssue(issue):
	try:
		cursor.execute('''
			INSERT INTO issue(bookID,patronID,librarianID,issueDate)
			VALUES(:bookID,:patronID,:librarianID,:issueDate)''', issue)
		connection.commit()
		return True
	except Exception as e:
		print(e)
		return False

def deleteIssue(issueID):
	try:
		cursor.execute('''DELETE FROM issue WHERE transID=?''', (issueID, ))
		connection.commit()
		return True
	except Exception as e:
		print(e)
		return False

def insertIssueHistory(issueHistory):
	try:
		cursor.execute('''
			INSERT INTO issue_history(transID,bookID,patronID,issuedbyID,returnedtoID,issueDate,returnDate,lateFees)
			VALUES(:transID,:bookID,:patronID,:issuedbyID,:returnedtoID,:issueDate,:returnDate,:lateFees)
			''', issueHistory)
		connection.commit()
		return True
	except Exception as e:
		return False

def queryIssueByBook(bookID, patron=False):
	try:
		if patron:
			cursor.execute('''
				SELECT transID,bookID,patronID,librarianID,issueDate,name 
				FROM issue,patron 
				WHERE patronID=patron.id AND bookID=?;''',(bookID, ))
		else:
			cursor.execute('''SELECT * FROM issue WHERE bookID=?''', (bookID, ))
		issue = cursor.fetchone()
		return issue
	except Exception as e:
		print(e)
		return None

def queryIssueHistoryByBook(bookID):
	try:
		cursor.execute('''SELECT transID,patronID,name,issueDate,returnDate 
			FROM issue_history,patron 
			WHERE patronID=patron.id AND bookID=?
			ORDER BY returnDate DESC, transID DESC;''', (bookID, ))
		issue_history = cursor.fetchall()
		return issue_history
	except Exception as e:
		print(e)
		return None

def getLatestIssues():
	try:
		cursor.execute('''SELECT transID,bookID,title,patronID,name,issueDate 
			FROM issue,book,patron 
			WHERE bookID=book.id AND patronID=patron.id 
			ORDER BY issueDate DESC, transID DESC;''')
		issues = cursor.fetchall()
		return issues
	except Exception as e:
		print(e)
		return None

def getLatestReturns():
	try:
		cursor.execute('''SELECT transID,bookID,title,patronID,name,returnDate 
			FROM issue_history,book,patron 
			WHERE bookID=book.id AND patronID=patron.id 
			ORDER BY returnDate DESC, transID DESC;''')
		returns = cursor.fetchall()
		return returns
	except Exception as e:
		print(e)
		return None

def queryBook(params):
	clause = []
	if params.get("title") is not None and params.get("title") is not '':
		clause.append("title LIKE '%{}%'".format(params.get("title")))
	if params.get("author") is not None and params.get("author") is not '':
		clause.append("author LIKE '%{}%'".format(params.get("author")))
	if params.get("isbn13") is not None and params.get("isbn13") is not '':
		clause.append("isbn13=:isbn13")
	if params.get("publisher") is not None and params.get("publisher") is not '':
		clause.append("publisher LIKE '%{}%'".format(params.get("publisher")))
	if params.get("supplierID") is not None and params.get("supplierID") is not '':
		clause.append("supplierID=:supplierID")
	if params.get("id") is not None and params.get("id") is not '':
		clause.append("id=:id")

	if clause:
		query = "SELECT * FROM book WHERE {}".format(" AND ".join(clause))
	else:
		query = "SELECT * FROM book"
	try:
		cursor.execute(query, params)
		book_list = cursor.fetchall()
		return book_list
	except Exception as e:
		print(e)
		return None

def querySupplier(params):
	clause = []
	if params.get("name") is not None and params.get("name") is not '':
		clause.append("name LIKE '%{}%'".format(params.get("name")))
	if params.get("supplierID") is not None and params.get("supplierID") is not '':
		clause.append("id=:supplierID")

	if clause:
		query = "SELECT * FROM supplier WHERE {}".format(" AND ".join(clause))
	else:
		query = "SELECT * FROM supplier"
	try:
		cursor.execute(query, params)
		supplier_list = cursor.fetchall()
		return supplier_list
	except Exception as e:
		print(e)
		return None

def queryPatron(params):
	clause = []
	if params.get("id") is not None and params.get("id") is not '':
		clause.append("id=:id")
	if params.get("name") is not None and params.get("name") is not '':
		clause.append("name LIKE '%{}%'".format(params.get("name")))
	if params.get("cardNum") is not None and params.get("cardNum") is not '':
		clause.append("id=:cardNum")
	if params.get("id") is not None and params.get("id") is not '':
		clause.append("id=:id")

	if clause:
		query = "SELECT * FROM patron WHERE {}".format(" AND ".join(clause))
	else:
		query = "SELECT * FROM patron"
	try:
		cursor.execute(query, params)
		patron_list = cursor.fetchall()
		return patron_list
	except Exception as e:
		print(e)
		return None

def getBookStatus(bookID):
	try:
		cursor.execute('''SELECT COUNT(*) FROM issue WHERE bookID=?''', (bookID, ))
		flag = cursor.fetchone()
		return flag[0] == 0
	except Exception as e:
		print(e)
		return None

def getBookExistence(bookID):
	try:
		cursor.execute('''SELECT COUNT(*) FROM book WHERE id=?''', (bookID,))
		flag = cursor.fetchone()
		return flag[0] == 1
	except Exception as e:
		print(e)
		return None

def getPatronExistence(patronID):
	try:
		cursor.execute('''SELECT COUNT(*) FROM patron WHERE id=?''', (patronID,))
		flag = cursor.fetchone()
		return flag[0] == 1
	except Exception as e:
		print(e)
		return None

def canPatronBorrow(patronID):
	try:
		cursor.execute('''SELECT COUNT(*) FROM issue WHERE patronID=?''', (patronID,))
		borrows = cursor.fetchone()[0]
		cursor.execute('''SELECT borrowLimit FROM patron WHERE id=?''', (patronID,))
		borrowLimit = cursor.fetchone()[0]
		return borrows<borrowLimit
	except Exception as e:
		print(e)
		return None

if __name__ == '__main__':
	book = {
		"title" : "American Gangster",
		"author" : "Max Allan Collins",
		"publishDate" : "02-10-2007",
		"publisher" : "Forge Books",
		"isbn13" :  "9780765359018",
		"supplierID" : "1"
	}
	# insertBook(book)
