from __future__ import print_function
import datetime
import scrapy
import time
import sys
import os

sys.path.append("_lib/")
from CsvHelper import CsvHelper
from UrlHelper import UrlHelper
import constants

__author__ = 'Jacek Aleksander Gruca'

# The field names of the output CSV file.
FIELD_NAMES = ['twitter_handle', 'twitter_url', 'timestamp', 'number_of_followers']

PREFIX = 'http://twitter.com/'


# This class represents the spider which will be run by Scrapy to scrape the number of followers from Twitter pages.
class TwitterScraper(scrapy.Spider):
	name = 'Twitter Scraper'

	# This variable is used by Scrapy to begin crawling.
	start_urls = []

	# This dictionary holds the mapping of the URLs to Twitter handles, which is used when populating the output file.
	url_map = {}

	# This list will contain all the URLs to visit and will pass them onto Scrapy in order, one by one.
	urls_to_visit = []

	# This method is the constructor of the spider-scraper. It takes in the names of the input and output files
	# and performs some pre-processing.
	def __init__(self, input_file=None, output_file=None):
		self.csv_helper = CsvHelper(FIELD_NAMES, input_file, output_file)
		if self.csv_helper.stop:
			print("\nINCORRECT INVOCATION, run as:\nscrapy runspider %s" % os.path.basename(__file__) + \
					" -a input_file=<your input file> -a output_file=<your output file>\n")
			return
		self.urlHelper = UrlHelper(PREFIX)
		self.urlHelper.process_urls_for_scrapy(self.csv_helper.get_input_file_content(),
															self.start_urls, self.url_map, self.urls_to_visit)

	# Here we override the method make_requests_from_url to use the one from the UrlHelper instead of the one in
	# scrapy.Spider
	def make_requests_from_url(self, url):
		return UrlHelper.make_requests_from_url(url)

	def parse(self, response):
		# Here we're in the method that performs the scraping. Below an xpath expression extracts the
		# number of followers from the element with attribute data-nav equal to "followers"
		followers_count = response.xpath('//*[@data-nav="followers"]/@title').re("[\d,]*")[0].replace(',', '')

		self.csv_helper.write_row_to_output_file(
			FIELD_NAMES,
			{FIELD_NAMES[0]: self.url_map[response.meta['start_url']], \
			 FIELD_NAMES[1]: response.meta['start_url'], \
			 FIELD_NAMES[2]: datetime.datetime.fromtimestamp(time.time()).strftime(constants.TIME_FORMAT), \
			 FIELD_NAMES[3]: followers_count})

		# If there are still URLs to process, then yield more crawling.
		if self.urls_to_visit:
			yield self.make_requests_from_url(self.urls_to_visit.pop(0))
