from __future__ import print_function

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import sendEmailConfig

__author__ = 'Jacek Aleksander Gruca'


# This class contains the email gateway processing required to send the email message via Mandrill.
class EmailGateway(object):
	# Send the message via the Mandrill account specified in the sendEmailConfig file.
	def send_message(self, message):
		msg = MIMEMultipart('alternative')
		msg['Subject'] = sendEmailConfig.MESSAGE_SUBJECT
		msg['From'] = sendEmailConfig.MESSAGE_FROM
		msg['To'] = sendEmailConfig.MESSAGE_TO
		body = MIMEText(message.print_message(), 'html')
		msg.attach(body)

		s = smtplib.SMTP(sendEmailConfig.SMTP_HOST, sendEmailConfig.SMTP_PORT)

		s.login(sendEmailConfig.MANDRILL_USERNAME, sendEmailConfig.MANDRILL_PASSWORD)
		s.sendmail(msg['From'], msg['To'], msg.as_string())
		print("Email sent to " + sendEmailConfig.MESSAGE_TO + ".")

		s.quit()
