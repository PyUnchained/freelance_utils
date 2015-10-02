import floppyforms.__future__ as forms

from collections import OrderedDict
import hashlib

from django.conf import settings
from django.contrib.auth.models import *
from django.forms import HiddenInput

from freelance_utils.money.models import *
from freelance_utils.money.utils import SHA256Hash


class OnlinePaymentForm(forms.ModelForm):

	ordered_field_names = ['type', 'amount']

	def __init__(self, *args, **kwargs):
		super(OnlinePaymentForm, self).__init__(*args, **kwargs)
		# Your field initialisation code
		self.rearrange_field_order()

	def rearrange_field_order(self):
		"""
		Re-orders the fields of the form depending on the ordered_field_names
		list.
		"""

		original_fields = self.fields
		new_fields = OrderedDict()

		for field_name in self.ordered_field_names:
			field = original_fields.get(field_name)
			if field:
				new_fields[field_name] = field

		self.fields = new_fields

	def clean(self):
		cleaned_data = super(CheckoutForm, self).clean()

		if cleaned_data['amount'] <= Decimal('0.00'):
			raise forms.ValidationError("Amount must be a positive value.")




	class Meta:
		model = OnlineTransaction
		exclude = ('date', 'is_verified', 'created_on', 'user')

class CheckoutForm(forms.Form):

	merchantid = forms.CharField(max_length = '100',
		widget = HiddenInput())
	orderid = forms.CharField(max_length = '100',
		widget = HiddenInput())
	signature = forms.CharField(max_length = '200')
	amount = forms.DecimalField(
		max_digits = 7,
		decimal_places = 2,
		widget = HiddenInput())
	redirect = forms.URLField(required = False, widget = HiddenInput())
	transferpending = forms.URLField(required = False, widget = HiddenInput())
	test = forms.BooleanField(initial = False)

	def clean(self, *args, **kwargs):

		cleaned_data = super(CheckoutForm, self).clean()

		hash_info = [settings.P4A_MERCHANT_ID,
			cleaned_data['orderid'],str(cleaned_data['amount']),
			settings.P4A_SECRET_KEY]

		if cleaned_data['signature'] != SHA256Hash(hash_info):
			raise forms.ValidationError("Invalid SHA256 Hash")

class VisibleCheckoutForm(forms.Form):


	amount = forms.DecimalField(
		max_digits = 7,
		decimal_places = 2)

