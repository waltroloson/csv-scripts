#!/bin/bash
#
# Author: Jacek Aleksander Gruca
#
# This script runs the scraping of Facebook and Twitter

export PYTHONPATH=.
export SCRAPY_SETTINGS_MODULE=settings

/usr/local/bin/scrapy runspider scrapeFacebook.py -a input_file=input/facebook.csv -a output_file=output/facebook.out.csv
echo
/usr/local/bin/scrapy runspider scrapeTwitterProfile.py -a input_file=input/twitter.csv -a output_file=output/twitter.out.csv
echo
python scrapeTwitterPhrase.py input/twitterSearch.csv output/twitter.out.csv
echo
/usr/local/bin/scrapy runspider scrapeInstagram.py -a input_file=input/instagram.csv -a output_file=output/instagram.out.csv
echo
/usr/local/bin/scrapy runspider scrapePinterest.py -a input_file=input/pinterest.csv -a output_file=output/pinterest.out.csv
echo
/usr/local/bin/scrapy runspider scrapeChromeExtensions.py -a input_file=input/chromestore.csv -a output_file=output/chromestore.out.csv
echo
/usr/local/bin/scrapy runspider scrapeiTunes.py -a input_file=input/itunes.csv -a output_file=output/itunes.out.csv
