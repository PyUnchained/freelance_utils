import logging
import smtplib
import time
import urllib
from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)

class MailComm:

	def __init__(self, to, subject, message, test = False):

		self.test = test

		#Possible exceptions to look for before trying to initialize
		if type(to) is not list:
			raise TypeError(
				"'To' argument must be a list of strings representing e-mail addresses")

		#Check to run 
		if not self.test:

			#First load all of the required settings
			try:
				self.sender = settings.EMAIL_HOST_USER
				self.host = settings.EMAIL_HOST
				self.host_port = settings.EMAIL_PORT
				self.displayed_name = settings.EMAIL_HOST_DISPLAYED_NAME
				self.host_pwd = settings.EMAIL_HOST_PASSWORD
				self.debug = settings.DEBUG
				self.error = None

			#If any of the settings are missing,
			#provide information on which settings are missing.
			except AttributeError, e:
				self.error = 'Missing Setting: ' + str(e)

		else:
			self.sender = 'test@test.com'
			self.host = 'smtp.test.com'
			self.host_port = 465
			self.displayed_name = 'Test'
			self.host_pwd = 'PWD'
			self.debug = True
			self.error = None


		self.to = to
		self.txt = str(message)
		self.subject = str(subject)
		self.msg = MIMEMultipart()

		self.msg['Subject'] = self.subject
		self.msg['From'] = formataddr(
			(str(Header(self.displayed_name, 'utf-8')),
			self.sender))

		self.msg['To'] = ", ".join(self.to)
		msg_txt = MIMEText(self.txt)
		self.msg.attach(msg_txt)


	def send(self):

		if self.debug and not self.test:
			return [1,'Ran in Test Mode']

		#Make sure there are no errors before trying to send
		if self.error:
			#Log the error msg
			logger.error(self.error)
			return [0, self.error]

		# Create server object with SSL option
		
		server = smtplib.SMTP_SSL(self.host,
				self.host_port)

		# Perform operations via server
		server.login(self.sender,
			self.host_pwd)
		server.sendmail(self.sender, self.to, self.msg.as_string())
		server.quit()

		#Log message sending
		logger_msg = """Email sent: {0}.""".format(
			{'HOST':self.host,
			'HOST_USER': self.sender,
			'PORT': self.host_port,
			'TIME':time.strftime("%c"),
			'TO':self.msg['To']})
		logger.info(logger_msg)

		return [1, {'HOST':self.host,
			'HOST_USER': self.sender,
			'PORT': self.host_port,
			'TIME':time.strftime("%c"),
			'TO':self.msg['To']}]

class SMSComm:

	def __init__(self, num_list, message, test = False):

		self.test = test
		#Load all of the required settings
		if not self.test:
			try:
				self.username = settings.SMS_USERNAME
				self.password = settings.SMS_PASSWORD
				self.sender = settings.SMS_SENDER
				self.url = settings.SMS_URL
				self.debug = settings.DEBUG
				self.error = None

			#If any of the settings are missing,
			#provide extra info.
			except AttributeError, e:
				self.error = 'Missing Setting: ' + str(e)

		else:
			self.username = 'test'
			self.password = 'pwd'
			self.sender = 263772111111
			self.url = 'test'
			self.debug = True
			self.error = None

		#Encode the parameters of the message
		self.message = str(message)
		self.num_list = num_list
		self.params = urllib.urlencode(
			{'username' : self.username,
			'password' : self.password,
			'message' : self.message,
			'msisdn' : ','.join(str(n) for n in self.num_list),
			'sender' : self.sender,
			'repliable' : 0})

		self.statusCode = '0'
		self.statusString = ''

	def get_bulksms_result(self):
		"""Gets results of attempted SMS sending through BulkSMS"""
		s = self.open_url.read()
		result = s.split('|')
		self.statusCode = str(result[0])
		self.statusString = str(result[1])
		

	def log_bulksms_result(self):
		"""Logs result messages for BulkSMS"""

		self.get_bulksms_result()
		#Log the response message
		if self.statusCode != '0':
			e_msg = "Error Sending SMS: " + self.statusCode + ": " + self.statusString
			logger.error(e_msg)
			return (1, e_msg)
		else:
			logger.info('SMS Sent: {0}'.format({
				'SENDER':self.sender,
				'DELIVERY_LIST':self.num_list,
				'TIME':time.strftime("%c"),
				'MESSAGE':self.message
				}))
			return (0,)

	def send(self):

		#Don't send an actual message if debug is on
		if self.debug and not self.test:
			return (0,'Ran in Test Mode')

		#Send message, log result and close
		self.open_url = urllib.urlopen(self.url, self.params)
		status = self.log_bulksms_result()
		self.open_url.close()

		return status

		
