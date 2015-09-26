import os
import csv

__author__ = 'Jacek Aleksander Gruca'


# This class provides CSV processing functions to code in which we want to abstract this processing out.
class CsvHelper(object):
	def __init__(self, field_names, input_file, output_file):

		self.stop = False
		# If the input_file or output_file were not specified or if the input_file is not present on filesystem
		# indicate to the calling code that we should stop here.
		if not input_file or not output_file or not os.path.isfile(input_file):
			self.stop = True
			return

		self.field_names = field_names
		self.input_file = input_file
		self.output_file = output_file

		# If the output file doesn't exist, create it and write the header row to it.
		if not os.path.isfile(output_file):
			self.write_header()

	# Populate the output file with the processed handle, source URL, timestamp and the item scraped.
	def write_row_to_output_file(self, fieldNames, parameterMap):
		with open(self.output_file, 'a+') as csvfile:
			self.csv_writer = csv.DictWriter(csvfile, self.field_names)
			self.csv_writer.writerow(parameterMap)

	# Write header to the output file.
	def write_header(self):
		with open(self.output_file, 'w+') as csvfile:
			self.csv_writer = csv.DictWriter(csvfile, self.field_names)
			self.csv_writer.writeheader()

	# Read input file into memory and return as a set of lines.
	def get_input_file_content(self):
		with open(self.input_file) as f:
			file_content = f.read()
		return file_content.split('\n')
