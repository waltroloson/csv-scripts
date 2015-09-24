from __future__ import print_function
import urllib2
import scrapy

__author__ = 'Jacek Aleksander Gruca'


# This class represents the spider which will be run by Scrapy to scrape the number of likes from pages.
class UrlHelper(object):
	# This method is the constructor of the scraper helper. It takes in the names of the input and output files
	# and performs some pre-processing of URLs.
	def __init__(self, prefix):
		self.prefix = prefix

	@staticmethod
	def make_requests_from_url(url):
		# A method that receives a URL and returns a Request object (or a list of Request objects) to scrape.
		# This method is used to construct the initial requests in the start_requests() method,
		# and is typically used to convert urls to requests.
		return scrapy.Request(url, dont_filter=True, meta={'start_url': url})

	def process_urls(self, handles, url_map, urls_to_visit):
		# Populate the map of URLs-to-handles and the list of URLs.
		for line in handles:
			handle_url = self.prefix + urllib2.quote(line.strip())
			url_map[handle_url] = line.strip()
			urls_to_visit.append(handle_url)

	def process_urls_for_scrapy(self, handles, start_urls, url_map, urls_to_visit):
		self.process_urls(handles, url_map, urls_to_visit)
		# Specify that the first URL to be scraped corresponds to the first handle read from the input file.
		start_urls.append(urls_to_visit.pop(0))
