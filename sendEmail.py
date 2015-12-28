from __future__ import print_function
import datetime
import urllib2
import json
import time
import sys
import re
import os
import csv
import dateutil.parser

sys.path.append("_lib/")
from EmailGateway import EmailGateway
from Message import Message
from Table import Table
import constants

__author__ = 'Jacek Aleksander Gruca'

# The field names of the output CSV file.
FIELD_NAMES = ['handle', 'url', 'timestamp', 'number_of_followers']


def processRow(filename, row, pMessage):
	table = pMessage.getTable(filename)
	table.addRow(row)
	print(table)


def processFile(filename, dateRange, pMessage):
	dFrom = datetime.datetime.strptime(dateRange.split("-")[0], "%Y%m%d").date()
	dTo = datetime.datetime.strptime(dateRange.split("-")[1], "%Y%m%d").date()
	print(dFrom)
	print(dTo)
	array = {}
	with open(filename, 'r') as csvfile:
		fileReader = csv.reader(csvfile, delimiter=',')
		next(fileReader, None)
		for row in fileReader:
			currentDate = dateutil.parser.parse(row[2]).date()
			print(currentDate)
			if (currentDate <= dTo and currentDate >= dFrom):
				processRow(filename, array, row, pMessage)


def print_usage():
	print("Run as:\npython %s <number of files> <input file 1> <date range 1> "
			"[<input file 2> <date range 2>  <input file 3> <date range 3> ...]" % os.path.basename(__file__))


# Here we check that the number of input parameters is even and equal to the number of files specified as input
if len(sys.argv) < 4 or sys.argv[1].isdigit() == False or len(sys.argv) != (int(sys.argv[1]) + 1) * 2:
	print_usage()
	exit(0)

numberOfFiles = int(sys.argv[1])

# print(numberOfFiles)

message = Message()
emailGateway = EmailGateway()

for i in range(numberOfFiles):
	filename = sys.argv[2 + 2 * i]
	dateRange = sys.argv[2 + 2 * i + 1]
	print("Processing file " + filename + " in date range " + dateRange)
	if (not re.match(r'^\d\d\d\d\d\d\d\d\-\d\d\d\d\d\d\d\d$', dateRange)):
		print(
			"Date range " + dateRange + " doesn't match pattern YYYYMMDD-YYYYMMDD. Date ranges are both left and right inclusive.")
		exit(0)
	processFile(filename, dateRange, message)

emailGateway.sendMessage(message)
