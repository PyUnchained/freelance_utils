import ast
import datetime
from django.test import TestCase
from decimal import Decimal
import hashlib
import autofixture
import json
import time


# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freelance_utils.tests.test_settings")


from django.conf import settings
from django.contrib.auth.models import User 
from django.core.urlresolvers import reverse

from freelance_utils.models import Account, Transaction, CallBackNotification
from freelance_utils.money.forms import*
from freelance_utils.money.utils import SHA256Hash
from freelance_utils.utils import is_negative, random_decimal_generator, random_text_generator

class MoneyTests(TestCase):
	"""
	Tests that the money functions all work.
	"""

	fixtures = ['freelance_utils/tests/fixtures_1.json']

	def test_save_method(self):
		"""
		Tests transaction objects:

		-Make sure save method converts positive values
		to negative ones for debit transactions
		"""
		
		#Test that the save function properly negates numbers.
		all_transactions = Transaction.objects.all()
		for item in all_transactions:
			item.save()

		#Test that all transaction objects were properly saved.
		account = Account.objects.get(pk = 1)
		self.assertEquals(len(account.history.all()), 4)

		for item in all_transactions:
			if item.type in ['D']:
				self.assertTrue(is_negative(item.amount))
			else:
				self.assertFalse(is_negative(item.amount))


	def test_transaction_objects(self):
		"""
		Test that the transact and transact_many methods work.
		"""

		
		account = Account.objects.get(pk = 1)
		account.check_bal(force = True)
		#See that the balances are being updated correctly 
		#and that the check_bal function works in force mode
		self.assertEquals(account.check_bal(), account.bal)

		#Make sure transactions are being added as soon as they are created
		cur_hist_length = len(account.history.all())
		new_transactions = autofixture.create(Transaction, 4,
			field_values={'amount': random_decimal_generator(),
			'user':account.user})

		self.assertEquals(len(account.history.all()), cur_hist_length + 4)

	def test_hash256_algorithm(self):

		#Hash info containing the amount as a Str, Decimal and Int
		#respectively.
		info = ['ilsaeducationcozw','jfjfkk345',str(Decimal('130.45')),
			'Y49A5POLDF17R5B83M76D6B6']
		info2 = ['ilsaeducationcozw','jfjfkk345',Decimal('130.45'),
			'Y49A5POLDF17R5B83M76D6B6']
		info3 = ['ilsaeducationcozw','jfjfkk345',130.45,
			'Y49A5POLDF17R5B83M76D6B6']

		#Test that the hash algorithm can handle decimal Str, Decimal or
		#Int objects respectivley
		self.assertTrue(SHA256Hash(info))
		self.assertTrue(SHA256Hash(info2))
		self.assertTrue(SHA256Hash(info3))

	def test_checkout_form(self):

		hash_info = [settings.P4A_MERCHANT_ID,'jfjfkk345',Decimal('130.45'),
			settings.P4A_SECRET_KEY]

		data = {'merchantid':hash_info[0],
			'orderid':hash_info[1],
			'signature':SHA256Hash(hash_info),
			'amount':hash_info[2],
			'test':True,
			'redirect':settings.P4A_REDIRECT_URL,
			'transferpending': settings.P4A_TRANSFER_PENDING_URL}

		form = CheckoutForm(data)
		self.assertTrue(form.is_valid())

		#Check that an incorrect signature raises validation error
		bad_data = {'merchantid':hash_info[0],
			'orderid':hash_info[1],
			'signature':'Pie',
			'amount':hash_info[2],
			'test':True,
			'redirect':settings.P4A_REDIRECT_URL,
			'transferpending': settings.P4A_TRANSFER_PENDING_URL}

		form = CheckoutForm(bad_data)
		self.assertFalse(form.is_valid())

	def test_P4A_confirmation(self):

		hash_info = [settings.P4A_MERCHANT_ID,random_text_generator(),random_decimal_generator(),
			settings.P4A_SECRET_KEY]
		digest = SHA256Hash(hash_info)

		#Check that no duplicate order ids are produced
		

		response = self.client.get(reverse('p4a_confirmation'),
			{
			'merchant': hash_info[0],
			'checkout':364775,
			'amount':hash_info[2],
			'email':'tatenda@gmail.com',
			'phone':'98349',
			'order':hash_info[1],
			'timestamp': int(time.time()),
			'digest': digest,
			})

		#Confirm the server responded and created an object with the right digest.
		self.assertEquals(response.status_code, 200)
		self.assertTrue(CallBackNotification.objects.get(
			digest = digest))
		#Check that confirmational JSON token was produced
		self.assertEquals(ast.literal_eval(response.content), {'status':1})

		hash_info = [settings.P4A_MERCHANT_ID,
			random_text_generator(),random_decimal_generator(),
			settings.P4A_SECRET_KEY]
		digest = SHA256Hash(hash_info)

		response = self.client.get(reverse('p4a_confirmation'),
			{
			'merchant': hash_info[0],
			'amount':hash_info[2],
			'order':hash_info[1],
			'timestamp': int(time.time()),
			'digest': digest,
			})
		self.assertEquals(response.status_code, 200)
		self.assertTrue(CallBackNotification.objects.get(
			digest = digest))
		#Check that confirmational JSON token was produced
		self.assertEquals(ast.literal_eval(response.content), {'status':1})


		response = self.client.get(reverse('p4a_confirmation'),
			{
			'merchant': hash_info[0],
			'amount':hash_info[2],
			'order':hash_info[1],
			'timestamp': 'pie',
			'digest': digest,
			})
		self.assertEquals(response.status_code, 200)
		#Check that error JSON token was produced
		self.assertEquals(ast.literal_eval(response.content), {'status':0})




		
