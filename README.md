# csv-scripts

To run the script for facebook likes: 

scrapy runspider scrapeFacebook.py -a input_file=<your input file> -a output_file=<your output file>

For example:

scrapy runspider scrapeFacebook.py -a input_file=facebook.csv -a output_file=facebooklikes.csv
