# csv-scripts

##### To run the script for Facebook likes:

scrapy runspider scrapeFacebook.py -a input_file=\<your input file> -a output_file=\<your output file>

For example:

scrapy runspider scrapeFacebook.py -a input_file=input/facebook.csv -a output_file=output/facebooklikes.csv

##### To run the script for Twitter followers:

scrapy runspider scrapeTwitterProfile.py -a input_file=\<your input file> -a output_file=\<your output file>

For example:

scrapy runspider scrapeTwitterProfile.py -a input_file=input/twitter.csv -a output_file=output/twitterfollowers.csv

##### To run the script for Twitter phrase tweets:

python scrapeTwitterPhrase.py \<your input file> \<your output file>

For example:

python scrapeTwitterPhrase.py input/twitterSearch.csv output/phrasetweets.csv
