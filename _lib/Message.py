from Table import Table
import sendEmailConfig

__author__ = 'Jacek Aleksander Gruca'

header = """
<!DOCTYPE HTML>
<html>
<head>
<META http-equiv="Content-Type" content="text/html; charset=utf-8">
<STYLE TYPE="text/css"> <!-- BODY {{ font-family:sans-serif; }}
	.cell {{ border-style: solid; border-width: 1px; border-color: rgb(219, 219, 219);
			padding: 10px; margin: 0px; width: 25%; }}
	.strong {{ font-weight: bold; font-size: 12px; }} --> </STYLE>
</head>
<body>
	<div style="word-wrap: break-word">
		<div>
			<div
			style="color: rgb(0, 0, 0); letter-spacing: normal; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px;">
				<div>
					<div
					style="font-family: Helvetica; font-style: normal; font-variant: normal; font-weight: normal; line-height: normal; font-size: 13px">
						<br>
						<br>
						<br>
						<div style="font-size: 12px">
							<div>
								<a href="{twitterUrl}" target="_blank">{twitterId}</a>
							</div>
							<div>
								<a href="{mailto}" target="_blank">{email}</a>
							</div>
							<div>
								<a href="{linkedinUrl}" target="_blank">{linkedinId}</a>
							</div>
							<div>
								<br>
							</div>
						</div>
					</div>
				</div>
				<br>
			</div>
			<br>
			<br>
		</div>
"""

footer = """
		</div>
	</div>
</body>
</html>
"""


# This class represents the email message which will be sent via an email gateway.
class Message(object):
	def __init__(self):
		self.tables = {}

	# Return the table corresponding to the appropriate input file. If the table has not yet been instantiated, create
	# it, store in the tables variable and return it.
	def get_table(self, filename):
		if filename in self.tables:
			return self.tables[filename]
		else:
			self.tables[filename] = Table(filename)
			return self.tables[filename]

	# Return the html code representing this Message object.
	def print_message(self):
		message = header.format(twitterUrl=sendEmailConfig.TWITTER_URL,
										twitterId=sendEmailConfig.TWITTER_ID,
										mailto=sendEmailConfig.MAILTO,
										email=sendEmailConfig.EMAIL,
										linkedinUrl=sendEmailConfig.LINKEDIN_URL,
										linkedinId=sendEmailConfig.LINKEDIN_ID)
		for filename in sorted(self.tables):
			message += self.tables[filename].print_table()
		message += footer
		return message
