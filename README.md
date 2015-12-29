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

##### To send a scraping report via Mandrill

Edit the file sendEmailConfig.py by specifying email sending confguration.

Run the sendEmail.py script in the following way:

python sendEmail.py <number of files> <input file 1> <date range 1> [<input file 2> <date range 2>  <input file 3> <date range 3> ...]

You can specify as many input files as you wish, but you should indicate how many there are in the first parameter to the script. Each file should be accompanied by a date range used to search it for relevant entries. The date range is inclusive and should be specified in the format YYYYMMDD-YYYYMMDD (from-to).