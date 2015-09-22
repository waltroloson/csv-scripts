from __future__ import print_function
from scrapy.selector import Selector
import scrapy
import os
import csv
import time
import datetime


__author__ = 'Jacek Aleksander Gruca'

# This constant is the current id of the HTML element containing the number of likes. If Facebook ever changes its
# layout or identifiers, at the very least this constant will need to be changed.
LIKES_ELEMENT_NAME = "PagesLikesCountDOMID"

# The field names of the output CSV file.
FIELD_NAMES = ['facebook_handle', 'facebook_url', 'timestamp', 'number_of_likes']

# This class represents the spider which will be run by Scrapy to scrape the number of likes from Facebook pages.
class FacebookScraper(scrapy.Spider):
	name = 'Facebook Scraper'

	# This variable is used by Scrapy to begin crawling.
	start_urls = []

	# This map holds the mapping of the URLs to Facebook handles, which is used when populating the output file.
	url_map = {}

	# This list will contain all the URLs to visit and will pass them onto Scrapy in order, one by one.
	urls = []

	# This method is the constructor of the spider-scraper. It takes in the names of the input and output files
	# and performs some preprocessing.
	def __init__(self, input_file=None, output_file=None):
		# If the input parameters don't match, print the below message for the user's benefit.
		if not input_file or not output_file:
			print("\nINCORRECT INVOCATION, run as:\nscrapy runspider %s" % os.path.basename(__file__) + \
					" -a input_file=<your input file> -a output_file=<your output file>\n")
			return

		# Populate the map of URLs to Facebook handles and the list of URLs.
		with open(input_file) as f:
			for line in f:
				facebook_url = 'http://facebook.com/' + line.strip()
				self.url_map[facebook_url] = line.strip()
				self.urls.append(facebook_url)

		# If the output file doesn't exist, write the header row to it.
		self.output_file = output_file
		if not os.path.isfile(output_file):
			with open(output_file, 'w+') as csvfile:
				self.csv_writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES)
				self.csv_writer.writeheader()

		# Specify that the first URL to be scraped corresponds to the first handle read from the input file.
		self.start_urls.append(self.urls.pop(0))

	def make_requests_from_url(self, url):
		# A method that receives a URL and returns a Request object (or a list of Request objects) to scrape.
		# This method is used to construct the initial requests in the start_requests() method,
		# and is typically used to convert urls to requests.
		return scrapy.Request(url, dont_filter=True, meta={'start_url': url})

	def parse(self, response):

		# Here we're in the method that performs the scraping. Below an xpath expression extracts all HTML comments
		# (it just so happens that the number of likes is in a comment)
		# from the Facebook page and narrows it down to the div containing the number of likes.
		comment = response.xpath('//comment()').re(r'<div.*%s.*/div>' % LIKES_ELEMENT_NAME)

		# Convert the text in the comment to HTML DOM object.
		comment_sel = Selector(text=comment[0], type="html")

		# Use XPATH to extract the final text with the number of likes.
		likesCount = (comment_sel.xpath('//*[@id="%s"]/*/text()' \
			% LIKES_ELEMENT_NAME).extract()[0]).replace(',', '').strip()

		# Populate the output file with the processed handle, Facebook URL, timestamp and the number of likes scraped.
		with open(self.output_file, 'a+') as csvfile:
			self.csv_writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES)
			self.csv_writer.writerow({'facebook_handle': self.url_map[response.meta['start_url']], \
				'facebook_url': response.meta['start_url'], \
				'timestamp' : datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), \
				'number_of_likes': likesCount})

		# If there are still URLs to process, then yield more crawling.
		if self.urls:
			yield self.make_requests_from_url(self.urls.pop(0))
