from __future__ import print_function
import urllib2
import scrapy

__author__ = 'Jacek Aleksander Gruca'


# This class provides URL processing functions to code in which we want to abstract this processing out.
class UrlHelper(object):

	# Construct URL helper and assign the prefix of the URLs.
	def __init__(self, prefix):
		self.prefix = prefix

	@staticmethod
	def make_requests_from_url(url):
		# A method that receives a URL and returns a Request object (or a list of Request objects) to scrape.
		# This method is used to construct the initial requests in the start_requests() method,
		# and is typically used to convert urls to requests.
		return scrapy.Request(url, dont_filter=True, meta={'start_url': url})

	# Populate the map of URLs-to-handles and the list of URLs.
	def process_urls(self, handles, url_map, urls_to_visit):
		for line in handles:
			line = line.strip()
			if "://" not in line:
				line = urllib2.quote(line)
			handle_url = self.prefix + line
			if isinstance(url_map, dict):
				url_map[handle_url] = line
			urls_to_visit.append(handle_url)

	# Perform regular processing and specify that the first URL to be scraped corresponds to the first item read from
	# the input file.
	def process_urls_for_scrapy(self, handles, start_urls, url_map, urls_to_visit):
		self.process_urls(handles, url_map, urls_to_visit)
		start_urls.append(urls_to_visit.pop(0))
