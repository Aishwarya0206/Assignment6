import requests
from bs4 import BeautifulSoup
import pandas
import argparse
import db

parser = argparse.ArgumentParser()
parser.add_argument("--page_num_max", help="Enter the number of pages to parse",type=int)
parser.add_argument("--dbname", help="Enter the name of db",type=str)
args = parser.parse_args()

flipkart_url = "https://www.flipkart.com/books/biographies-memoirs-and-general-nonficton-books/biographies-and-autobiographies/pr?count=40&sid=bks%2Cwmz%2Ckdl&p%5B%5D=facets.fulfilled_by%255B%255D%3DFlipkart%2BAssured&otracker=clp_banner_1_8.bannerX3.BANNER_the-non-fiction-store_1B8GED41POYU&fm=neo%2Fmerchandising&iid=M_6165dfa3-40f1-4047-8844-dfc8a5acd610_8.1B8GED41POYU&ppt=clp&ppn=the-non-fiction-store&ssid=tsw82x8on40000001603958891167&page="
page_num_MAX = args.page_num_max
scrapped_info_list = []
db.connect(args.dbname)

for page_num in range(1,page_num_MAX):
	url = flipkart_url + str(page_num)
	print("GET Request for: " + url)
	req = requests.get(url)
	content = req.content

	soup = BeautifulSoup(content,"html.parser")
	all_books = soup.find_all("div",{"class":"_3liAhj"})
	
	for books in all_books:
		book_dict = {}
		book_dict["name"] = books.find("a",{"class":"_2cLu-l"}).text
		book_dict["price"] = books.find("div",{"class":"_1vC4OE"}).text
		try:
			book_dict["author"] = books.find("div",{"class":"_1rcHFq"}).text
			book_dict["offer"] = books.find("div",{"class":"VGWI6T"}).text
			book_dict["org_price"] = books.find("div",{"class":"_3auQ3N"}).text
			book_dict["review"] = books.find("div",{"class":"hGSR34"}).text
			book_dict["review_given"] = books.find("span",{"class":"_38sUEc"}).text
		except AttributeError:
			book_dict["author"] = None
			book_dict["offer"] = None
			book_dict["org_price"] = None
			book_dict["review"] = None
			book_dict["review_given"] = None
		finally:
			scrapped_info_list.append(book_dict)
			db.insert_into_table(args.dbname, tuple(book_dict.values()))

dataframe = pandas.DataFrame(scrapped_info_list)
print("Creating a csv file ...")
dataframe.to_csv("flipkart.csv")
db.get_book_info(args.dbname)

	
