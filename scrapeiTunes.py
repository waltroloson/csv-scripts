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
FIELD_NAMES = ['itunes_url', 'timestamp', 'current_rating', 'no_of_current_reviews', 'cumulative_rating',
					'no_of_all_reviews']


# This class represents the spider which will be run by Scrapy to scrape the reviews from iTunes pages.
class iTunesScraper(scrapy.Spider):
	name = 'iTunes Scraper'

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
		self.url_helper = UrlHelper("")  # no prefix
		self.url_helper.process_urls_for_scrapy(self.csv_helper.get_input_file_content(),
															 self.start_urls, None, self.urls_to_visit)

	def make_requests_from_url(self, url):
		return UrlHelper.make_requests_from_url(url)

	def parse(self, response):

		fullStars = len(response.xpath("//div[@id='left-stack']/div[2]/div[2]/div[1]/span[@class='rating-star']"))
		halfStars = len(response.xpath("//div[@id='left-stack']/div[2]/div[2]/div[1]/span[@class='rating-star half']"))
		ghostStars = len(response.xpath("//div[@id='left-stack']/div[2]/div[2]/div[1]/span[@class='rating-star ghost']"))

		reviewCount = response.xpath("//div[@id='left-stack']/div[2]/div[2]/span[2]/text()").extract_first()
		reviewCount = reviewCount.strip()[:-8]

		fullStarsAll = len(response.xpath("//div[@id='left-stack']/div[2]/div[4]/div[1]/span[@class='rating-star']"))
		halfStarsAll = len(response.xpath("//div[@id='left-stack']/div[2]/div[4]/div[1]/span[@class='rating-star half']"))
		ghostStarsAll = len(
			response.xpath("//div[@id='left-stack']/div[2]/div[4]/div[1]/span[@class='rating-star ghost']"))

		reviewCountAll = response.xpath("//div[@id='left-stack']/div[2]/div[4]/span[1]/text()").extract_first()
		reviewCountAll = reviewCountAll.strip()[:-8]

		message = None
		if fullStars + halfStars + ghostStars != 5 or fullStarsAll + halfStarsAll + ghostStarsAll != 5:
			message = "Error scraping page, scraping skipped."

		self.csv_helper.write_row_to_output_file(
			FIELD_NAMES,
			{FIELD_NAMES[0]: response.meta['start_url'], \
			 FIELD_NAMES[1]: datetime.datetime.fromtimestamp(time.time()).strftime(constants.TIME_FORMAT), \
			 FIELD_NAMES[2]: fullStars + 0.5 * halfStars if not message else message,
			 FIELD_NAMES[3]: reviewCount if not message else None,
			 FIELD_NAMES[4]: fullStarsAll + 0.5 * halfStarsAll if not message else None,
			 FIELD_NAMES[5]: reviewCountAll if not message else None})

		# If there are still URLs to process, then yield more crawling.
		if self.urls_to_visit:
			yield self.make_requests_from_url(self.urls_to_visit.pop(0))
