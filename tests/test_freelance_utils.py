import unittest
from smtplib import SMTP_SSL
from mock import patch, call
import mock

from django.core.exceptions import *
from freelance_utils.comms import MailComm, SMSComm
from freelance_utils.tests.utils import is_lib_available



class TestComms(unittest.TestCase):
	"""
	Tests the communications utilities (e-mail, sms)
	"""


	def test_mail_comm(self):
		"""
		Test mail object:

		-Initializes properly
		-Sends and quits server
		"""
		to = ['cathytambo@ilsaeducation.co.zw',
			'jmukwedeya@ilsaeducation.co.zw',
			'tatendatambo@gmail.com']
		subject = 'Testing'
		message = 'Test message'

		to_output = ", ".join(to)


		#Check that an attribute error is raised if any key settings are missing
		#Only runs if django dependencies are present
		if is_lib_available('django.conf.settings'):
			with self.assertRaises(AttributeError) as e:
				MailComm(to,subject, message)

		with patch("smtplib.SMTP_SSL") as mock_smtp:
            # Build test message
			test_subject = MailComm(to,subject, message, test = True)
			#Check correctly formatted to string
			self.assertEqual(test_subject.msg['To'], to_output)
			res = test_subject.send()

		#Check that all server calls were made till server disconnect.
		instance = mock_smtp.return_value
		self.assertTrue(instance.login.called)
		self.assertTrue(instance.sendmail.called)
		self.assertTrue(instance.quit.called)
	
	
	@patch.object(SMSComm, 'get_bulksms_result')
	def test_sms_comm(self, mock_get_bulksms_result):
		"""
		Test SMS Communication:
		-Initialize SMS
		-Open, send and close connection
		"""

		#The list contains a mixture of integers and text to
		#make sure both are equivalent
		num_list = [263772111111, '263772111111', 263772111111]
		message = 'This is just a test message'

		#Check that an attribute error is raised if any key settings are missing
		#Only runs if django dependencies are present
		if is_lib_available('django.conf.settings'):
			with self.assertRaises(AttributeError) as e:
				SMSComm(num_list, message)


		with patch("urllib.urlopen") as mock_urllib:
			test_subject = SMSComm(num_list, message, test = True)
			status = test_subject.send()

			#Check that the mock url call was made successfully, status was sent
			#and connection terminated
			instance = mock_urllib.return_value
			self.assertEqual(status[0], 0)
			self.assertTrue(instance.close.called)

			#Check that failure statuses are working
			test_subject.statusCode = '1'
			status = test_subject.send()
			self.assertEqual(status[0], 1)
			


if __name__ == '__main__':
    unittest.main()