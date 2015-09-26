from __future__ import print_function
import datetime
import urllib2
import json
import time
import sys
import re
import os

sys.path.append("_lib/")
from CsvHelper import CsvHelper
from UrlHelper import UrlHelper
import constants

__author__ = 'Jacek Aleksander Gruca'

# The field names of the output CSV file.
FIELD_NAMES = ['twitter_phrase', 'topsy_url', 'timestamp', 'number_of_tweets']


def print_usage():
	print("Run as:\npython %s <input file> <output file>" % os.path.basename(__file__))

if len(sys.argv) != 3:
	print_usage()
	exit(0)

# This dictionary holds the mapping of the URLs to Twitter phrases, which is used when populating the output file.
url_map = {}

# This list will contain all the URLs to visit.
urls_to_visit = []

# Create CsvHelper which will aid in processing the CSV files
csv_helper = CsvHelper(FIELD_NAMES, sys.argv[1], sys.argv[2])
if csv_helper.stop:
	print_usage()
	exit(0)

# Here we take the system's current time and convert it to the number of seconds since the 'epoch'.
# Further on we subtract the number of seconds in 24 hours from it and specify the result
# as the time from which the number of tweets should be counted.
current_time = time.mktime(time.localtime())
time_24_hours_ago = current_time - constants.SECONDS_IN_24H_COUNT
time_query_parameter = "&mintime=" + repr(int(time_24_hours_ago))

# Create the UrlHelper which will aid in processing URLs
url_helper = UrlHelper(
	'http://otter.topsy.com/searchcount.js?dynamic=1&count_method=citation&' +
	'apikey=09C43A9B270A470B8EB8F2946A9369F3&%s&q=' % time_query_parameter)
url_helper.process_urls(csv_helper.get_input_file_content(), url_map, urls_to_visit)

print("Scraping number of tweets for phrases..")

# For each URL in the list of URLs to visit connect to topsy and fetch a response containing JSON
# with all the numbers of tweets in the past periods. From it we extract the number of tweets in
# the past day and write a line in the output CSV file.
for url in urls_to_visit:
	topsy_response = urllib2.urlopen(url).read()
	json_response = re.search("\{.*\}", topsy_response).group(0)
	tweets_count = json.loads(json_response)['response']['windows']['d']['total']

	csv_helper.write_row_to_output_file(
		FIELD_NAMES,
		{FIELD_NAMES[0]: url_map[url], \
		 FIELD_NAMES[1]: url, \
		 FIELD_NAMES[2]: datetime.datetime.fromtimestamp(current_time).strftime(constants.TIME_FORMAT), \
		 FIELD_NAMES[3]: tweets_count})

print("Done.")
