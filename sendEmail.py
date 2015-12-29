from __future__ import print_function
import dateutil.parser
import datetime
import sys
import re
import os
import csv

sys.path.append("_lib/")
from EmailGateway import EmailGateway
from Message import Message
from Table import Table
import constants

__author__ = 'Jacek Aleksander Gruca'

# The field names of the output CSV file.
FIELD_NAMES = ['handle', 'url', 'timestamp', 'number_of_followers']


# Add a row to the appropriate table in the message object.
def processRow(filename, row, pMessage):
	table = pMessage.get_table(filename)
	table.add_row(row)


# Process the file containing scraped data.
def processFile(filename, dateRange, pMessage):
	# Parse the date range to be searched into dFrom and dTo.
	dFrom = datetime.datetime.strptime(dateRange.split("-")[0], "%Y%m%d").date()
	dTo = datetime.datetime.strptime(dateRange.split("-")[1], "%Y%m%d").date()
	with open(filename, 'r') as csvfile:
		fileReader = csv.reader(csvfile, delimiter=',')
		next(fileReader, None)  # skip the header
		for row in fileReader:
			currentDate = dateutil.parser.parse(row[2]).date()
			# Only process a row of input if it's in the provided date range.
			if (currentDate >= dFrom and currentDate <= dTo):
				processRow(filename, row, pMessage)


def print_usage():
	print("Run as:\npython %s <number of files> <input file 1> <date range 1> "
			"[<input file 2> <date range 2>  <input file 3> <date range 3> ...]" % os.path.basename(__file__))


# Here we check that the number of input parameters is even and equal to the number of files specified as input
if len(sys.argv) < 4 or sys.argv[1].isdigit() == False or len(sys.argv) != (int(sys.argv[1]) + 1) * 2:
	print_usage()
	exit(0)

# Here we store the number of files specified as input and instantiate the message object which will be sent by the
# emailGateway object using the Mandrill account specified in the sendEmailConfig file.
numberOfFiles = int(sys.argv[1])
message = Message()
emailGateway = EmailGateway()

# Process the input parameters and validate that the input ranges are in a correct format.
for i in range(numberOfFiles):
	filename = sys.argv[2 + 2 * i]
	dateRange = sys.argv[2 + 2 * i + 1]
	print("Processing file " + filename + " in date range " + dateRange)
	if (not re.match(r'^\d\d\d\d\d\d\d\d\-\d\d\d\d\d\d\d\d$', dateRange)):
		print(
			"Date range " + dateRange + " doesn't match pattern YYYYMMDD-YYYYMMDD."
												 " Date ranges are both left and right inclusive.")
		exit(0)
	processFile(filename, dateRange, message)

emailGateway.send_message(message)
