import dateutil.parser
import re

__author__ = 'Jacek Aleksander Gruca'

header = """
		<div>
			<br/>
		</div>
		<div>
			<div
				style="font-family: &amp; #39; Helvetica Neue&amp;#39;; font-size: 11px">
				<br/>
			</div>
			<table
				style="border-collapse: collapse; width: 100%; table-layout: fixed; margin-left: 0px; font-family: &amp; #39; Helvetica Neue&amp;#39;; font-size: 11px;">
				<tbody>
"""

footer = """
				</tbody>
			</table>
			<div
				style="font-family: &amp; #39; Helvetica Neue&amp;#39;; font-size: 11px;"></div>
"""


# This class represents a table in the message corresponding to an input .csv file provided.
class Table(object):
	def __init__(self, filename):
		self.filename = filename
		self.map = {}

	# Ingest a row of input by storing its values in the two-dimensional map object.
	def add_row(self, fields):
		currentDate = dateutil.parser.parse(fields[2]).date()
		# if (re.match(r'.*//twitter\.com.*', fields[1])) or True
		self.map[currentDate, fields[0]] = fields[3]

	# Return the html code representing this Table object.
	def print_table(self):

		html = header

		dates = []
		identifiers = []

		for key in sorted(self.map):
			date, identifier = key
			dates.append(date)
			identifiers.append(identifier)

		dates = sorted(set(dates))
		identifiers = sorted(set(identifiers))

		style = """border-style: solid; border-width: 1px; border-color: rgb(219, 219, 219);
			padding: 10px; margin: 0px;"""
		style_strong = style + " font-weight: bold; font-size: 12px;"

		html += """<tr><td style="{style1}">{filename1}</td>""".format(filename1=self.filename, style1=style_strong)
		for identifier in identifiers:
			html += """<td style="{style1}">{identifier1}</td>""".format(identifier1=identifier, style1=style)
		html += "</tr>"

		for date in dates:
			html += """<tr><td style="{style1}">{date1}</td>""".format(date1=date, style1=style)
			for identifier in identifiers:
				html += """<td style="{style1}">{value1}</td>""". \
					format(value1=self.map[date, identifier] if (date, identifier) in self.map else "", style1=style)
			html += "<tr/>"

		return html + footer
