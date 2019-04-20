class Input_field_test:
	"""
	Test types: (String) username, password, email, phonenumber
	Return: A list that contains
	  'pass' if input fields passes,
	  'fail' if input field fails,
	  'invalid value' if invalid values are given,
	  'empty' if input fields are empty
	The idea is to check output length, if its more than one, it's a fail
	"""


	def empty_test_pass(self, input_value):
		"""
		Private method
		Returns True if input_value is not an empty string, False otherwise
		"""
		if input_value==None:
			return False
		else:
			return True


	def numbers_only(self, input_value):
		"""
		Private method
		Returns True if characters in input_value string is only numbers, False otherwise
		"""
		output = True
		for i in input_value:
			if ord(i) >= 48 and ord(i) <= 57:
				# character is number
				pass
			else:
				output = output and False
		return output


	def alphabets_numbers_space_only(self, input_value):
		"""
		Private method
		Returns True if characters in input_value string is only alphabets, numbers and space, False otherwise
		ord values of characters:
		a - 97
		z - 122
		A - 65
		Z - 90
		0 - 48
		9 - 57
		space - 32
		Note: The " " character fails the test
		"""
		output = True
		for i in input_value:
			if ord(i) >= 97 and ord(i) <= 122:
				# character is small capital alphabet
				pass
			elif ord(i) >= 65 and ord(i) <= 90:
				# character is large capital alphabet
				pass
			elif ord(i) >= 48 and ord(i) <= 57:
				# character is number
				pass
			elif ord(i) == 32:
				# character is space
				pass
			else:
				output = output and False
		return output


	def username(self, input_value):
		"""
		Public method
		Returns True if input_value is not empty string, and only contains alphabets and numbers
		"""
		output = []
		pass_fail_state = True

		if not self.empty_test_pass(input_value):
			if pass_fail_state:
				pass_fail_state = False
				output.append("fail")
			output.append("empty")
			return output

		if not self.alphabets_numbers_space_only(input_value):
			if pass_fail_state:
				pass_fail_state = False
				output.append("fail")
			output.append("invalid value")

		if pass_fail_state:
			output.append("pass")

		return output



	def password(self, input_value):
		"""
		Public method
		Returns True if input_value is not empty string
		"""
		output = []
		pass_fail_state = True

		if not self.empty_test_pass(input_value):
			if pass_fail_state:
				pass_fail_state = False
				output.append("fail")
			output.append("empty")
			return output

		if pass_fail_state:
			output.append("pass")

		return output


	def email(self, input_value):
		"""
		Public method
		Returns True if input_value is not empty string, input_value
		  contains only alphabets and numbers, and one '@'
		"""
		output = []
		pass_fail_state = True
		email_addr_count = 0

		if not self.empty_test_pass(input_value):
			if pass_fail_state:
				pass_fail_state = False
				output.append("fail")
			output.append("empty")
			return output

		for i in input_value:
			if ord(i) >= 97 and ord(i) <= 122:
				# character is small capital alphabet
				pass
			elif ord(i) >= 65 and ord(i) <= 90:
				# character is large capital alphabet
				pass
			elif ord(i) >= 48 and ord(i) <= 57:
				# character is number
				pass
			elif ord(i) == 46:
				# character is .
				pass
			elif ord(i) == 64:
				# character is @
				email_addr_count += 1
			else:
				pass_fail_state = False

		if pass_fail_state and email_addr_count == 1:
			output.append("pass")
		else:
			output.append("fail")
			output.append("invalid value")

		return output


	def phonenumber(self, input_value):
		"""
		Public method
		Return True if characters in input_value is only numbers and input_value is not empty string, False otherwise
		"""
		output = []
		pass_fail_state = True

		if not self.empty_test_pass(input_value):
			if pass_fail_state:
				pass_fail_state = False
				output.append("fail")
			output.append("empty")
			return output

		if not self.numbers_only(input_value):
			if pass_fail_state:
				pass_fail_state = False
				output.append("fail")
			output.append("invalid value")

		if pass_fail_state:
			output.append("pass")

		return output

	def ticket_title(self, input_value):
		"""
		Public method
		Return True if input_value is empty, False otherwise
		"""
		output = []
		pass_fail_state = True

		if not self.empty_test_pass(input_value):
			if pass_fail_state:
				pass_fail_state = False
				output.append("fail")
			output.append("empty")
			return output

		if pass_fail_state:
			output.append("pass")

		return output


	def ticket_description(self, input_value):
		"""
		Public method
		Return True if input_value is empty, False otherwise
		"""
		output = []
		pass_fail_state = True

		if not self.empty_test_pass(input_value):
			if pass_fail_state:
				pass_fail_state = False
				output.append("fail")
			output.append("empty")
			return output

		if pass_fail_state:
			output.append("pass")

		return output


	def ticket_id(self, input_value):
		"""
		Public method
		Return True if input_value is empty, False otherwise
		"""
		pass


	def token(self, input_token):
		"""
		Public method
		For verifying that the post request reaching to our remote_create in ticket_create
		is from one of the remote forms we've created
		"""
		output = []
		pass_fail_state = True

		forms_token = "UKJHhgvIU&^%$bvd#$HJ"
		token_list = [forms_token]

		if input_token in token_list:
			pass_fail_state = True
			output.append("pass")
		else:
			pass_fail_satte = False
			output.append("fail")
			output.append("invalid value")

		return output


