# import external modules
import os
import urllib.parse
from requests_html import HTMLSession

# import application modules
from src.helpers.request_params import set_page_number
from src.helpers.request_utils import get_product_info_html, get_product_info_html_with_proxy, get_reviews_html, get_reviews_html_with_proxy
from src.helpers.constants import Constants
from src.proxy import *
from src.helpers.utils import export_to_file

class Scraper:
    _save_dir: str
    _session: HTMLSession
    _proxy: Proxy

    def __init__(self, session: HTMLSession, save_dir: str, proxy: Proxy = None):
        self._session = session
        self._save_dir = save_dir
        self._proxy = proxy
    


    def scrape_product_data(self, product_asin: str, url: str):
        #print info
        print('Getting product info ...')

        # get product info from the helper function
        product_info = get_product_info_html_with_proxy(session=self._session, url=url, proxy_generator=self._proxy) if self._proxy else get_product_info_html(session=self._session, url=url)

        # get file name for saving prduct information
        filename = Constants.PRODUCT_DATA_FILE_NAME.replace('asin', product_asin)

        # add folder path to the file
        filename = os.path.join(f'./src/generated_data/html_data/{self._save_dir}', filename)

        # export product data to file
        export_to_file(filename, str(product_info))



    def scrape_reviews_data(self, product_asin: str, url: str, params: dict[str, str], keyword: str = ''):
        # save all the reviews generated from each page
        all_reviews = []

        # loop through all the pages
        for page in range(1, Constants.MAX_PAGES + 1):
            # print info
            print('Getting reviews for page: ' + str(page))

            #set page to params
            set_page_number(params=params, page=page)

            # generate final url by appending params
            target_url = url + "?" + urllib.parse.urlencode(params)

            # get all the reviews from the url
            reviews = get_reviews_html_with_proxy(session=self._session, url=target_url, proxy_generator=self._proxy) if self._proxy else get_reviews_html(session=self._session, url=target_url) 

            # if no reviews are found for the request, break - indicates than no more reviews are available
            if len(reviews) == 0:
                break
            
            # append the page reviews to all reviews
            all_reviews += reviews

        # get the file name for saving the reviews
        filename = Constants.REVIEWS_DATA_FILE_NAME.replace('asin_keyword', f"{product_asin}_{keyword}")

        # add folder path to the file
        filename = os.path.join(f'./src/generated_data/html_data/{self._save_dir}', filename)

        # export product data to file
        export_to_file(filename, str(all_reviews))

        # print total revies scraped
        print("Total Reviews: ", len(all_reviews))