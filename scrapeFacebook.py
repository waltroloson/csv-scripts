from __future__ import print_function
from scrapy.selector import Selector
import scrapy
import time
import datetime
import sys
import os

sys.path.append("_lib/")
from CsvHelper import CsvHelper
from UrlHelper import UrlHelper
import constants

__author__ = 'Jacek Aleksander Gruca'

# The field names of the output CSV file.
FIELD_NAMES = ['facebook_handle', 'facebook_url', 'timestamp', 'number_of_likes']

PREFIX = 'http://facebook.com/'

# This constant is the current id of the HTML element containing the number of likes. If Facebook ever changes its
# layout or identifiers, at the very least this constant will need to be changed.
LIKES_ELEMENT_NAME = "PagesLikesCountDOMID"


# This class represents the spider which will be run by Scrapy to scrape the number of likes from Facebook pages.
class FacebookScraper(scrapy.Spider):
	name = 'Facebook Scraper'

	# This variable is used by Scrapy to begin crawling.
	start_urls = []

	# This dictionary holds the mapping of the URLs to Facebook handles, which is used when populating the output file.
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
		self.url_helper = UrlHelper(PREFIX)
		self.url_helper.process_urls_for_scrapy(self.csv_helper.get_input_file_content(),
															 self.start_urls, self.url_map, self.urls_to_visit)

	def make_requests_from_url(self, url):
		return UrlHelper.make_requests_from_url(url)

	def parse(self, response):
		# Here we're in the method that performs the scraping. Below an xpath expression extracts all HTML comments
		# (it just so happens that the number of likes is in a comment)
		# from the Facebook page and narrows it down to the div containing the number of likes.
		comment = response.xpath('//comment()').re(r'<div.*%s.*/div>' % LIKES_ELEMENT_NAME)

		# Convert the text in the comment to HTML DOM object.
		comment_sel = Selector(text=comment[0], type="html")

		# Use XPATH to extract the final text with the number of likes.
		likes_count = (comment_sel.xpath('//*[@id="%s"]/*/text()' \
													% LIKES_ELEMENT_NAME).extract()[0]).replace(',', '').strip()

		self.csv_helper.write_row_to_output_file(
			FIELD_NAMES,
			{FIELD_NAMES[0]: self.url_map[response.meta['start_url']], \
			 FIELD_NAMES[1]: response.meta['start_url'], \
			 FIELD_NAMES[2]: datetime.datetime.fromtimestamp(time.time()).strftime(constants.TIME_FORMAT), \
			 FIELD_NAMES[3]: likes_count})

		# If there are still URLs to process, then yield more crawling.
		if self.urls_to_visit:
			yield self.make_requests_from_url(self.urls_to_visit.pop(0))
