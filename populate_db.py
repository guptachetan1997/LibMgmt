import pandas as pd
import random
import db_util

def populateBooks():
	supps = [1,2,3,4,5]
	books = pd.read_csv('books.csv')
	suppIDS = [random.choice(supps) for book in books.values]
	books['supplierID'] = suppIDS

	dicts = books.to_dict(orient='records')

	for book in dicts:
		db_util.insertBook(book)		

if __name__ == '__main__':
	main()