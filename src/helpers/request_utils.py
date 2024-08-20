import time
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from src.helpers.constants import Constants
from src.proxy import Proxy
from src.helpers.utils import get_headers


def get_product_info_html(session: HTMLSession, url: str) -> str:
	"""Get product information from the web request

	Params:
	@session: `HTMLSession` session object for the web request
	@url: `str` containing the request url

	Returns:
	Product information HTML from the request response
	"""
	# number of tries to hit the request before giving up, when the response does not contain the expected data
	times = Constants.MAX_TRIES

	# response data
	productInfo = ""
    
	# run until max tries are not reached
	while times > 0:
        # decrement times
		times -= 1

		# sleep for some time before each call in the loop
		time.sleep(0.01)
        
		# get headers object with new random user agent for the call
		headers = get_headers()

		# get response from the request
		response = session.get(url, headers=headers)

		# if resonse does not contain expected data continue until max tries are exhausted
		if "api-services-support@amazon.com" in response.text:
			continue
		
		

		# generate a soup object from the response data
		soup = BeautifulSoup(response.content, 'lxml')

		# extract product info div
		productInfo = soup.select_one('div[id="cm_cr-product_info"]')

		# break out of the loop, indicating that we have found the expected data
		break
	
	# return product info html data
	return productInfo



def get_product_info_html_with_proxy(session: HTMLSession, url: str, proxy_generator: Proxy) -> str:
	"""Get product information from the web request using proxies from proxy server

	Params:
	@session: `HTMLSession` session object for the web request
	@url: `str` containing the request url
    @proxy_generator: `Proxy` object, returning the proxy generated from the proxy server

	Returns:
	Product information HTML from the request response
	"""
	# number of tries to hit the request before giving up, when the response does not contain the expected data
	times = Constants.MAX_TRIES

	# response data
	productInfo = ""

	# get proxy from the proxy generator
	proxies = proxy_generator.get_proxy()
    
	# run until max tries are not reached
	while times > 0:
		# decrement times
		times -= 1

		# sleep for some time before each call in the loop
		time.sleep(0.01)

		# get headers object with new random user agent for the call
		headers = get_headers()
		
		# get response from the request
		response = session.get(url=url, headers=headers, proxies=proxies)

		# if resonse does not contain expected data continue until max tries are exhausted
		if "api-services-support@amazon.com" in response.text:
			continue

		# generate a soup object from the response data
		soup = BeautifulSoup(response.content, 'lxml')

		# extract product info div
		productInfo = soup.select_one('div[id="cm_cr-product_info"]')

		# break out of the loop, indicating that we have found the expected data
		break
	
	# return product info html data
	return productInfo



def get_reviews_html(session: HTMLSession, url: str):
	"""Get product revews from the web request

	Params:
	@session: `HTMLSession` session object for the web request
	@url: `str` containing the request url

	Returns:
	Product reveiews HTML from the request response
	"""
	# number of tries to hit the request before giving up, when the response does not contain the expected data
	times = Constants.MAX_TRIES

	# reviews object to save the revies
	reviews = []

	# run until max tries are not reached
	while times > 0:
		#decrement times
		times -= 1

		# sleep for some time before each call in the loop
		time.sleep(0.01)

		# get headers object with new random user agent for the call
		headers = get_headers()
		
		# get response from the request
		response = session.get(url=url, headers=headers)

		# if resonse does not contain expected data continue until max tries are exhausted
		if "api-services-support@amazon.com" in response.text:
			continue
		
		# generate a soup object from the response data
		soup = BeautifulSoup(response.content, 'lxml')

		# extract review divs and append to the result object 
		reviews = soup.select('div[data-hook="review"]')
		
		# break out of the loop, indicating that we have found the expected data
		break

	# print information about the requests and responses
	print("Tries remain: ", times)
	print("Reviews generated: ", len(reviews))
	print(response.url)

	# return product reviews html
	return reviews



def get_reviews_html_with_proxy(session: HTMLSession, url: str, proxy_generator: Proxy):
	"""Get product reviews from the web request using proxies from proxy server

	Params:
	@session: `HTMLSession` session object for the web request
	@url: `str` containing the request url
    @proxy_generator: `Proxy` object, returning the proxy generated from the proxy server

	Returns:
	Product reviews HTML from the request response
	"""
	# number of tries to hit the request before giving up, when the response does not contain the expected data
	times = Constants.MAX_TRIES

	# reviews object to save the revies
	reviews = []

	# get proxy from the proxy generator
	proxies = proxy_generator.get_proxy()

	# run until max tries are not reached
	while times > 0:
		#decrement times
		times -= 1

		# sleep for some time before each call in the loop
		time.sleep(0.01)

		# get headers object with new random user agent for the call
		headers = get_headers()
		
		# get response from the request
		response = session.get(url=url, headers=headers, proxies=proxies)

		# if resonse does not contain expected data continue until max tries are exhausted
		if "api-services-support@amazon.com" in response.text:
			continue
		
		# generate a soup object from the response data
		soup = BeautifulSoup(response.content, 'lxml')

		# extract review divs and append to the result object 
		reviews = soup.select('div[data-hook="review"]')
		
		# break out of the loop, indicating that we have found the expected data
		break

	# print information about the requests and responses
	print("Tries remain: ", times)
	print("Reviews generated: ", len(reviews))
	print(response.url)

	# return product reviews html
	return reviews