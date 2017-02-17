from flask import Flask, render_template, request, redirect, flash
import db_util
app = Flask(__name__)

@app.route("/addbook", methods=["POST", "GET"])
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
			flash("Error in data entered.")
			return redirect("/addbook")
		else:
			return redirect("/")

@app.route("/addsupplier", methods=["POST", "GET"])
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
			flash("Error in data entered.")
			return redirect("/apply")
		else:
			return redirect("/")


@app.route("/")
def home():
	params = {}
	books = db_util.queryBook(params)
	return render_template("home.html", payload={"books":books})

if __name__ == "__main__":
	app.secret_key = '%qufh2ea8!-$%_ctzw=in*d2__i#s*3_mph82!+(3m9g*!%@tt'
	app.config['SESSION_TYPE'] = 'filesystem'
	app.run()