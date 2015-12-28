from Table import Table

__author__ = 'Jacek Aleksander Gruca'


# This class represents the email message which will be sent via an email gateway.
class Message(object):
	tables = {}

	def __init__(self):
		print()

	def addHeadlineTwitter(self, text, link):
		print()

	def addHeadlineEmail(self, text, link):
		print()

	def addHeadlineLinkedIn(self, text, link):
		print()

	def getTable(self, filename):
		if (filename in self.tables):
			return self.tables[filename]
		else:
			self.tables[filename] = Table()
			return self.tables[filename]
