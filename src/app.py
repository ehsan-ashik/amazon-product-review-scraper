# import external modules
import os
from dotenv import load_dotenv

# import application modules
from src.session import Session
from src.helpers.request_params import get_params
from src.helpers.constants import Constants
from src.proxy import SmartProxy
from src.parsers.csv_parser import CSVParser
from src.parsers.json_parser import JSONParser
from src.scraper import Scraper
from src.config import AppConfig


def scrape(product_asin, keywords, url, session, proxy):
	print("Scraping started...")
	# scrape product and Review Data from the Request and Save them into htmls
	#initiate scraper
	scraper = Scraper(session=session, save_dir=AppConfig.product_category, proxy=proxy)

	# scape product info
	scraper.scrape_product_data(product_asin=product_asin, url=url)

	# scrape review data
	for keyword in keywords:
		# get request params
		params = get_params(reviewer_type=AppConfig.reviewer_type,
					 sort_by=AppConfig.sort_by, 
					 filter_by_star=AppConfig.filter_by_star, keyword=keyword)
		
		# scrape review data
		scraper.scrape_reviews_data(product_asin=product_asin, url=url, params=params, keyword=keyword)
	
	# get filtered review based on amazon star filters
	if AppConfig.filtered_reviews:
		# get request params
		for filter_by_star in AppConfig.filters:

			params = get_params(reviewer_type=AppConfig.reviewer_type,
					 sort_by=AppConfig.sort_by, 
					 filter_by_star=filter_by_star)	
			
			print('Filter by star value:', str(filter_by_star))
			
			scraper.scrape_reviews_data(product_asin=product_asin, url=url, params=params, keyword=str(filter_by_star))

	print("Scraping completed...")
	print('---------------------------------------------\n\n')


def parse(product_asin, keywords, parser):
	print("Parsing started...")
	# Parse Product info and review scraped data and save then into json 
	# parse product and review info
	parser.parse_product_info(product_asin=product_asin)

	# parse files for each keyword
	for keyword in keywords:
		parser.parse_product_reviews(product_asin=product_asin, keyword=keyword, only_english_reviews=AppConfig.only_english_reviews)

	# parse files for each filter
	if AppConfig.filtered_reviews:
		for filter_by_star in AppConfig.filters:
			parser.parse_product_reviews(product_asin=product_asin, keyword=str(filter_by_star), only_english_reviews=AppConfig.only_english_reviews)

	print("Parsing completed...")



# main function for the project
def main():
	# Initialize and configure the project modules
	# load environment variables and proxy creds
	load_dotenv()
	# get request session
	session = Session()
	# initialize proxy variable
	proxy = SmartProxy(os.environ.get('SMARTPROXY_USERNAME'), os.environ.get('SMARTPROXY_PASSWORD')) if AppConfig.use_proxy else None

	# input data
	keywords = AppConfig.keywords

	# scrape
	if AppConfig.scrape_task:
		for product_asin in AppConfig.product_asins:
			# generate the URL for to call
			url = f"{Constants.BASE_URL}{product_asin}"

			scrape(product_asin, keywords, url, session, proxy)

	# parse
	if AppConfig.parse_task:
		# initiate parser
		if AppConfig.use_csv_parser:
			# csv parser
			parser = CSVParser(AppConfig.product_category)

			for product_asin in AppConfig.product_asins:
				parse(product_asin, keywords, parser)
			# save the data as csv
			parser.save_csv()
		else:
			# json parser
			parser = JSONParser(AppConfig.product_category)

			for product_asin in AppConfig.product_asins:
				parse(product_asin, keywords, parser)
			# save the data as json
			parser.save_json()