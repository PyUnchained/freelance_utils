import datetime
from decimal import*
import pickle
import time


from django.db import models, IntegrityError
from django.contrib import admin
from django.contrib.auth.models import User

from freelance_utils.models import Account
from freelance_utils.utils import random_text_generator

def order_code_generator():
	#Generates a unique order code by storing all used codes in
	#a file and reading from the list of used codes.
	used_codes = pickle.load( open( "order_code.dat", "rb" ) )
	unique = False

	while True:
		code = random_text_generator()
		if code not in used_codes:
			used_codes.append(code)
			pickle.dump(used_codes, open( "order_code.dat", "wb" ) )
			return code


class TransferPendingNotification(models.Model):

	merchant = models.CharField(max_length = 50)
	order = models.CharField(max_length = 100, null = True)
	digest = models.CharField(max_length = 100, null = True)

	def save(self, *args, **kwargs):

		if type(self.merchant) == type([]):
			self.merchant = self.merchant[0]
			self.order = self.order[0]
			self.digest =self.digest[0]

		super(TransferPendingNotification, self).save(*args, **kwargs)


class CallBackNotification(models.Model):

	merchant = models.CharField(max_length = 50)
	checkout = models.CharField(max_length = 50, null = True)
	order = models.CharField(max_length = 100, null = True, unique = True)
	amount = models.DecimalField(
		max_digits = 7,
		decimal_places = 2,
		null = True)
	email = models.EmailField(null = True)
	phone = models.IntegerField(null = True)
	timestamp = models.DateTimeField(null = True)
	digest = models.CharField(max_length = 100, null = True)

	is_confirmed = models.BooleanField(default = False)
	is_verified = models.BooleanField(default = False)


	def save(self, *args, **kwargs):

		#Since the values from GET requests are parses as lists,
		#this selects the actul value itself, not the list
		#(which would otherwise throw an error)
		data_dict = kwargs.pop('data_dict', None)

		if data_dict:
			self.verify(data_dict)


		#Deal with the checkout and phone number's first, as these may or may
		#not be present in the GET request sent from P4A
		try:
			if self.checkout:
				self.checkout = self.checkout[0]
			if self.phone:
				self.phone = self.phone[0]
			if self.email:
				self.email = self.email[0]
			
			self.merchant = self.merchant[0]
			self.order = self.order[0]
			self.amount = Decimal(self.amount[0])
			if type(self.timestamp[0]) != type(datetime.datetime.now()):
				self.timestamp = datetime.datetime.fromtimestamp(
					float(self.timestamp[0]))
			self.digest =self.digest[0]
		
		except TypeError:

			if type(self.timestamp) != type(datetime.datetime.now()):
				self.timestamp = datetime.datetime.fromtimestamp(
					float(self.timestamp))


		
		super(CallBackNotification, self).save(*args, **kwargs)


	def verify(self,data_dict):

		#Verifies that all of the expected data from the Pay4App
		#server came through.
		expected = ['merchant', 'checkout', 'order', 'amount',
			'email', 'timestamp', 'digest']
		dict_keys = data_dict.keys()

		for item in expected:
			if item not in dict_keys:
				self.is_verified = False
				return False

		self.is_verified = True
		return True

class P4APayment(models.Model):
	
	order = models.CharField(max_length = 20, null = True, unique = True, blank = True)
	digest = models.CharField(max_length = 200, null = True)
	call_back = models.ForeignKey('CallBackNotification', null = True, blank = True)

	def save(self, *args, **kwargs):

		self.order = order_code_generator()
		super(P4APayment, self).save(*args, **kwargs)





class BaseTransaction(models.Model):

	amount = models.DecimalField(
		max_digits = 7,
		decimal_places = 2)
	date = models.DateTimeField()
	created_on = models.DateTimeField(auto_now_add = True)
	user = models.ForeignKey(User)

	def save(self, *args, **kwargs):
		"""
		Custom save method

		- Make all debit values negative
		- Make all credit and refund values positive
		"""

		self.negate_decimal(self.amount)

		super(BaseTransaction, self).save(*args, **kwargs) # Call the "real" save() method.
		
		#Then find the target user's account and add the transaction to it.
		account = Account.objects.get(user = self.user)
		account.transact(self)
		account.save()

	def negate_decimal(self, num):

		if self.type == 'D':
			if num > Decimal('0.00'):
				num = Decimal('0.00') - num
		else:
			if num < Decimal('0.00'):
				num = num - num*2

	def __str__(self):

		#Get the displayed name for the transaction type
		for t in self.TYPES:
			if self.type == t[0]:
				type_display_name = t[1]

		return type_display_name + ' of $' +str(self.amount)+ ' on ' + self.date.strftime('%d %b, %Y')


class Transaction(BaseTransaction):
	TYPES = (
		('C', 'Credit'),
		('D', 'Debit'),
		('R', 'Refund')
		)

	type = models.CharField(max_length = 1, choices = TYPES)



class OnlineTransaction(BaseTransaction):

	TYPES = (
		('AT','Academics Tuition'),
		('PT', 'Professional Tuition'),
		('ET','ECD Tuition'),
		('AE','Academics Exam/Practical'),
		('PE','Professionals Exam/Practical'),
		('O','Other'))

	type = models.CharField(max_length = 2, choices = TYPES)

	is_verified = models.BooleanField(default = False)		


@admin.register(Transaction, OnlineTransaction,
	CallBackNotification, TransferPendingNotification,
	P4APayment)
class FreelanceMoneyAdmin(admin.ModelAdmin):
    pass