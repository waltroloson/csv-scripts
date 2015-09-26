#!/bin/bash
#
# Author: Jacek Aleksander Gruca
#
# This script runs the scraping of Facebook and Twitter

scrapy runspider scrapeFacebook.py -a input_file=input/facebook.csv -a output_file=output/facebooklikes.csv
echo
scrapy runspider scrapeTwitterProfile.py -a input_file=input/twitter.csv -a output_file=output/twitter.csv
echo
python scrapeTwitterPhrase.py input/twitterSearch.csv output/twitter.csv
