from __future__ import print_function
from scrapy.selector import Selector
import datetime
import scrapy
import time
import sys
import os
import re

sys.path.append("_lib/")
from CsvHelper import CsvHelper
from UrlHelper import UrlHelper
import constants

__author__ = 'Jacek Aleksander Gruca'

# The field names of the output CSV file.
FIELD_NAMES = ['chrome_extension_url', 'timestamp', 'number_of_users']


# This class represents the spider which will be run by Scrapy to scrape the number of users from Chrome
# Extensions pages.
class ChromeScraper(scrapy.Spider):
	name = 'Chrome Scraper'

	# This variable is used by Scrapy to begin crawling.
	start_urls = []

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
		self.url_helper = UrlHelper("") # no prefix
		self.url_helper.process_urls_for_scrapy(self.csv_helper.get_input_file_content(),
															 self.start_urls, None, self.urls_to_visit)

	def make_requests_from_url(self, url):
		return UrlHelper.make_requests_from_url(url)

	def parse(self, response):
		# This method parses each of the pages found under the urls_to_visit and extracts the number
		# of users from each of them
		p = re.compile('.*name\s*=\s*"user_count"\s*>\s*(\d+)\s*<')
		body = response.body_as_unicode().split('\n')

		userCount = None
		for line in body:
			m = p.match(line)
			if m:
				userCount = m.group(1)

		self.csv_helper.write_row_to_output_file(
			FIELD_NAMES,
			{FIELD_NAMES[0]: response.meta['start_url'], \
			 FIELD_NAMES[1]: datetime.datetime.fromtimestamp(time.time()).strftime(constants.TIME_FORMAT), \
			 FIELD_NAMES[2]: userCount})

		# If there are still URLs to process, then yield more crawling.
		if self.urls_to_visit:
			yield self.make_requests_from_url(self.urls_to_visit.pop(0))
