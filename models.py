from decimal import*

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, NoReverseMatch

class Account(models.Model):

	user = models.ForeignKey(User)
	user_number = models.CharField(max_length = 12, null = True)
	bal = models.DecimalField(
		max_digits = 10,
		decimal_places = 2,
		default = Decimal(0.00)
		)

	history = models.ManyToManyField('Transaction', blank = True)
	elearning_active = models.BooleanField(default = False)
	payments_active = models.BooleanField(default = False)

	last_modified = models.DateTimeField(auto_now = True)

	def check_bal(self, force = None):

		check_bal = Decimal(0.00)
		for item in self.history.all():
			check_bal = check_bal + item.amount

			if force:
				self.bal = check_bal
				self.save()

		return check_bal



	def transact(self, transaction):


		if transaction in self.history.all():
			return [3,'Transaction already recorded.']

		self.bal = self.bal + transaction.amount
		self.history.add(transaction)
		self.save()
		return [1, 'Processed successfully']

	def transact_many(self, transaction):

		history = self.history.all()
		print history

		for item in transaction:
			if item in history:
				pass

			else:
				#Save the item first to make sure the debit transaction
				#values are converted to negative numbers
				item.save()
				self.bal = self.bal + item.amount
				self.history.add(item)
		
		self.save()
		
		return [1, 'Processed successfully']


	def __str__(self):
		return self.user.username + ' ' + str(self.pk)

@admin.register(Account)
class FreelanceMoneyAdmin(admin.ModelAdmin):
    pass


from money.models import *