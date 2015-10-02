from collections import OrderedDict
import string
import random
from decimal import Decimal



def is_negative(value):
		if Decimal(str(value)) < Decimal(0):
			return True
		else:
			return False

def random_text_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def random_decimal_generator(digit_num = 5, place_num = 2, nums = string.digits):

	digit = ''.join(random.choice(nums) for _ in range(digit_num-place_num))
	digit = digit + '.'
	digit = digit + ''.join(random.choice(nums) for _ in range(place_num))
	return Decimal(digit)

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