from __future__ import print_function

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import sendEmailConfig
import smtplib

__author__ = 'Jacek Aleksander Gruca'


# This class represents the email message which will be sent via an email gateway.
class EmailGateway(object):
	# Send the message via the Mandrill account specified in the sendEmailConfig file.
	def send_message(self, message):
		f = open('myfile.html', 'w')
		print(message.print_message(), file=f)

		msg = MIMEMultipart('alternative')

		msg['Subject'] = sendEmailConfig.MESSAGE_SUBJECT
		msg['From'] = sendEmailConfig.MESSAGE_FROM
		msg['To'] = sendEmailConfig.MESSAGE_TO
		body = MIMEText(message.print_message(), 'html')
		msg.attach(body)

		s = smtplib.SMTP('smtp.mandrillapp.com', 587)

		s.login(sendEmailConfig.MANDRILL_USERNAME, sendEmailConfig.MANDRILL_PASSWORD)
		s.sendmail(msg['From'], msg['To'], msg.as_string())
		print("Email sent to " + sendEmailConfig.MESSAGE_TO + ".")

		s.quit()
