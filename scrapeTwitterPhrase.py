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

FIELD_NAMES = ['twitter_phrase', 'topsy_url', 'timestamp', 'number_of_tweets']

if len(sys.argv) != 3:
	print("Run as:\npython %s <input file> <output file>" % os.path.basename(__file__))
	exit(0)

# This dictionary holds the mapping of the URLs to Twitter phrases, which is used when populating the output file.
url_map = {}

# This list will contain all the URLs to visit.
urls_to_visit = []

csv_helper = CsvHelper(FIELD_NAMES, sys.argv[1], sys.argv[2])

current_time = time.mktime(time.localtime())
time_24_hours_ago = current_time - constants.SECONDS_IN_24H_COUNT
time_query_parameter = "&mintime=" + repr(int(time_24_hours_ago))

url_helper = UrlHelper(
	'http://otter.topsy.com/searchcount.js?dynamic=1&count_method=citation&' +
	'apikey=09C43A9B270A470B8EB8F2946A9369F3&%s&q=' % time_query_parameter)
url_helper.process_urls(csv_helper.get_input_file_content(), url_map, urls_to_visit)

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
