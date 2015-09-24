import os
import csv

__author__ = 'Jacek Aleksander Gruca'


class CsvHelper(object):
	def __init__(self, field_names, input_file, output_file):

		self.stop = False
		if not input_file or not output_file:
			self.stop = True
			return

		self.field_names = field_names
		self.input_file = input_file
		self.output_file = output_file

		# If the output file doesn't exist, create it and write the header row to it.
		if not os.path.isfile(output_file):
			self.write_header()

	# Populate the output file with the processed handle, Facebook URL, timestamp and the number of likes scraped.
	def write_row_to_output_file(self, fieldNames, parameterMap):
		with open(self.output_file, 'a+') as csvfile:
			self.csv_writer = csv.DictWriter(csvfile, self.field_names)
			self.csv_writer.writerow(parameterMap)

	def write_header(self):
		with open(self.output_file, 'w+') as csvfile:
			self.csv_writer = csv.DictWriter(csvfile, self.field_names)
			self.csv_writer.writeheader()

	def get_input_file_content(self):
		with open(self.input_file) as f:
			file_content = f.read()
		return file_content.split('\n')
