import sqlite3

def connect(dbname):
	conn = sqlite3.connect(dbname)

	conn.execute("CREATE TABLE IF NOT EXISTS FLIPKART_BOOKS (NAME TEXT,  PRICE TEXT, AUTHOR TEXT, OFFER TEXT, ORG_PRICE TEXT, REVIEW TEXT, REVIEWS_GIVEN TEXT)")

	print("Table created successfully...")

	conn.close()

def insert_into_table(dbname, values):
	conn = sqlite3.connect(dbname)
	print("Inserted into table: "+str(values))
	insert_sql = "INSERT INTO FLIPKART_BOOKS (NAME, PRICE, AUTHOR, OFFER, ORG_PRICE, REVIEW, REVIEWS_GIVEN) VALUES (?, ?, ?, ?, ?, ?, ?)"
	conn.execute(insert_sql, values)
	conn.commit()
	conn.close()

def get_book_info(dbname):
	conn = sqlite3.connect(dbname)
	cur = conn.cursor()
	cur.execute("SELECT * FROM FLIPKART_BOOKS")
	table_data = cur.fetchall()
	for rec in table_data:
		print(rec)