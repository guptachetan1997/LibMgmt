from flask import Flask, render_template, request, redirect, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
import db_util
from librarian import Librarian
import datetime
import random

app = Flask(__name__)
app.secret_key = '%qufh2ea8!-$%_ctzw=in*d2__i#s*3_mph82!+(3m9g*!%@tt'
app.config['SESSION_TYPE'] = 'filesystem'
LATE_FINE = 5
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"

def calcLateFees(issueDate, returnDate):
	lateFees = 0
	date1OBJ = datetime.datetime.strptime(issueDate, "%d-%m-%Y")
	date2OBJ = datetime.datetime.strptime(returnDate, "%d-%m-%Y")
	days_issued = (date2OBJ-date1OBJ).days
	if days_issued>7:
		lateFees = (days_issued-7)*LATE_FINE
	return lateFees

def generate():
	caNum = random.randint(100000, 999999)
	if db_util.isUniqueCardNumber(caNum):
		return caNum
	else:
		generate()

def validate(thing):
	return thing != "" and thing != None

@login_manager.user_loader
def user_loader(username):
	return Librarian().get(username)

@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		form_data = request.form
		username = form_data.get("username")
		password = form_data.get("password")
		if validate(username) and validate(password):
			librarian = Librarian()
			librarian = librarian.get(username)
			if librarian:
				if bcrypt.check_password_hash(librarian.password, password):
					librarian.authenticated = True
					login_user(librarian)
					return redirect('/')
			else:
				flash("Incorrect Credentials.", "danger")
	return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
	librarian = current_user
	librarian.authenticated = False
	logout_user()
	return redirect("/")

@app.route("/addbook", methods=["POST", "GET"])
@login_required
def addBook():
	if request.method == "GET":
		return render_template("addBook.html")
	if request.method == "POST":
		form_data = request.form
		book = {
		"title" : form_data.get('title'),
		"author" : form_data.get('author'),
		"publishDate" : form_data.get('publishDate'),
		"publisher" : form_data.get('publisher'),
		"isbn13" :  form_data.get('isbn13'),
		"supplierID" : form_data.get('supplierID')
		}
		status = db_util.insertBook(book)
		if status == False:
			flash("Error in data entered.", "danger")
			return redirect("/addbook")
		else:
			return redirect("/")

@app.route("/addsupplier", methods=["POST", "GET"])
@login_required
def addSupplier():
	if request.method == "GET":
		return render_template("addsupplier.html")
	if request.method == "POST":
		form_data = request.form
		supplier = {
		"name" : form_data.get('name'),
		"phone" : form_data.get('phone'),
		"address" : form_data.get('address'),
		}
		status = db_util.insertSupplier(supplier)
		if status == False:
			flash("Error in data entered.")
			return redirect("/addsupplier")
		else:
			return redirect("/")

@app.route("/searchbook", methods=["POST", "GET"])
def searchBook():
	if request.method == "GET":
		return render_template("searchbook.html", payload={"type":"book"})
	if request.method == "POST":
		form_data = request.form
		if request.method == "POST":
			form_data = request.form
			book = {
			"title" : form_data.get('title'),
			"author" : form_data.get('author'),
			"publisher" : form_data.get('publisher'),
			"isbn13" :  form_data.get('isbn13'),
			"supplierID" : form_data.get('supplierID')
			}
			books = db_util.queryBook(book)
			statuses = []
			for bookOBJ in books:
				statuses.append(db_util.getBookStatus(bookOBJ[0]))
			return render_template("searchbook.html", payload={"books":books, "statuses":statuses})

@app.route("/searchsupplier", methods=["POST", "GET"])
@login_required
def searchSupplier():
	if request.method == "GET":
		return render_template("searchsupplier.html", payload={"type":"supplier"})
	if request.method == "POST":
		form_data = request.form
		if request.method == "POST":
			form_data = request.form
			supplier = {
			"name" : form_data.get('name'),
			"supplierID" : form_data.get('supplierID'),
			}
			suppliers = db_util.querySupplier(supplier)
			return render_template("searchsupplier.html", payload={"suppliers":suppliers})

@app.route("/searchpatron", methods=["POST", "GET"])
@login_required
def searchPatron():
	if request.method == "GET":
		return render_template("searchpatron.html", payload={"type":"patron"})
	if request.method == "POST":
		form_data = request.form
		if request.method == "POST":
			form_data = request.form
			patron = {
			"id" : form_data.get('id'),
			"name" : form_data.get('name'),
			"cardNum" : form_data.get('cardNum'),
			}
			patrons = db_util.queryPatron(patron)
			return render_template("searchpatron.html", payload={"patrons":patrons})

@app.route("/apply", methods=["POST", "GET"])
def patronApply():
	if request.method == "GET":
		return render_template("apply.html")
	if request.method == "POST":
		pass
		form_data = request.form
		patron_form = {
		"name" : form_data.get('name'),
		"dob" : form_data.get('dob'),
		"address" : form_data.get('address'),
		"phone" : form_data.get('phone')
		}
		status = db_util.insertPatronReg(patron_form)
		if status == False:
			flash("Error in data entered.", "danger")
			return redirect("/apply")
		else:
			return redirect("/")

@app.route("/applications")
@login_required
def patronApplications():
	applications = db_util.queryPatronReg()
	return render_template("applications.html", payload={"applications":applications})

@app.route("/reject/<int:regID>")
@login_required
def rejectApplication(regID):
	flag = db_util.deletePatronReg(regID)
	if flag is False:
		flash("Error in rejecting.", "danger")		
	return redirect("/applications")

@app.route("/accept/<int:regID>")
@login_required
def acceptApplication(regID):
	regis_req_patron = db_util.querySinglePatronReg(regID)
	if regis_req_patron is not None:
		patron = {
			"cardNum" : generate(),
			"doj" : datetime.datetime.today().strftime("%d-%m-%Y"),
			"borrowLimit" : 2,
			"name": regis_req_patron[1],
			"dob": regis_req_patron[2],
			"address": regis_req_patron[3],
			"phone": regis_req_patron[4]
		}
		flag = db_util.insertPatron(patron)
		db_util.deletePatronReg(regID)
		if flag is False:
			flash("Error in Accepting.", "danger")
		return redirect("/applications")

@app.route("/issuereturn", methods=["GET"])
@login_required
def isseureturn():
	return render_template("issuereturn.html")

@app.route("/issue", methods=["POST"])
@login_required
def issueBook():
	if request.method == "POST":
		form_data = request.form
		issueRequest = {
		"bookID" : form_data.get('bookID'),
		"patronID" : form_data.get('patronID'),
		"librarianID" : form_data.get('librarianID'),
		"issueDate" : datetime.datetime.today().strftime("%d-%m-%Y")
		}
		book_exists = db_util.getBookExistence(issueRequest.get("bookID"))
		patron_exists = db_util.getPatronExistence(issueRequest.get("patronID"))
		if book_exists is True:
			if patron_exists is True:
				book_status = db_util.getBookStatus(issueRequest.get("bookID"))
				can_patron_borrow = db_util.canPatronBorrow(issueRequest.get("patronID"))
				if book_status is True:
					if can_patron_borrow is True:
						insert_status = db_util.insertIssue(issueRequest)
						flash("Book issued Successfully", "success")
						if insert_status is False:
							flash("Error in Issueing.", "danger")
					else:
						flash('Patron cannot borrow more.', "danger")
				else:
					flash("Book is Issued.", "danger")
			else:
				flash("Patron does not exist.", "danger")
		else:
			flash("Book does not Exist.", "danger")
		return redirect('/issuereturn')

@app.route("/return", methods=["POST"])
@login_required
def returnBook():
	if request.method == "POST":
		form_data = request.form
		returnRequest = {
			"bookID" : form_data.get("bookID"),
			"returnedtoID" : form_data.get("librarianID"),
		}
		issue = db_util.queryIssueByBook(returnRequest.get("bookID"))
		if issue is not None:
			returnRequest["transID"] = issue[0]
			returnRequest["patronID"] = issue[2]
			returnRequest["issuedbyID"] = issue[3]
			returnRequest["issueDate"] = issue[4]
			returnRequest["returnDate"] = datetime.datetime.today().strftime("%d-%m-%Y")
			returnRequest["lateFees"] = calcLateFees(returnRequest["issueDate"],returnRequest["returnDate"])
			flag = db_util.insertIssueHistory(returnRequest)
			if flag is False:
				flash("Error in Returning")
			else:
				db_util.deleteIssue(returnRequest["transID"])
				if returnRequest["lateFees"] > 0:
					flash("You have to pay {} Rs. as fine.".format(returnRequest["lateFees"]), "success")
				else:
					flash("Book Returned Successfully", "success")
		else:
			flash("Book is not Issued yet.", "danger")
	return redirect("/issuereturn")

@app.route("/book/<int:bookID>")
@login_required
def bookInfo(bookID):
	payload = {}
	book_exists = db_util.getBookExistence(bookID)
	payload["book_exists"] = book_exists
	if book_exists is True:
		payload['book_info'] = db_util.queryBook({"id":bookID})[0]
		payload['book_status'] = db_util.getBookStatus(bookID)
		payload['issue_history'] = db_util.queryIssueHistoryByBook(bookID)
		payload['issued_to'] = db_util.queryIssueByBook(bookID,patron=True)
	return render_template("bookinfo.html", payload=payload)

@app.route("/patron/<int:patronID>")
@login_required
def patronInfo(patronID):
	payload = {}
	patron_exists = db_util.getPatronExistence(patronID)
	payload["patron_exists"] = patron_exists
	if patron_exists is True:
		payload["patron_info"] = db_util.queryPatron({"id":patronID})[0]
		payload["issues"] = db_util.getPatronIssues(patronID)
	return render_template("patroninfo.html", payload=payload)

@app.route("/")
def home():
	payload = {}
	if current_user.is_authenticated is not False:
		latest_issues = db_util.getLatestIssues()
		latest_returns = db_util.getLatestReturns()
		payload['issues'] = latest_issues
		payload['returns'] = latest_returns
	return render_template("home.html", payload=payload)

if __name__ == "__main__":
	app.run()