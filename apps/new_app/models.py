from __future__ import unicode_literals
from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
	def validation(self, first_name, last_name, email, password, confirm_password):
		email_regex = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
		messages = []
		valid = True
		if len(first_name) < 2 or len(first_name) > 25 or len(last_name) < 2 or len(last_name) > 25:
			valid = False
			messages.append('First name/last name must be less than 25 characters and more than 1 character!')
		if not re.match(email_regex, email):
			valid = False
			messages.append('Invalid email format!')
		if password == '' or len(password) < 6:
			valid = False
			messages.append('Password must be longer than 5 characters')
		if password != confirm_password:
			valid = False
			messages.append("Passwords don't match")
		if len(User.userManager.filter(email=email)) != 0:
			valid = False
			messages.append("Email already exists")
		if valid:
			return (True, 'valid')
		else:
			return (False, messages)

class SecretManager(models.Manager):
	def validation(self, secret):
		if secret == '':
			return (False, 'Please enter something!')
		else:
			return (True, 'Success')

class User(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.CharField(max_length=30)
	password = models.CharField(max_length=255)
	userManager = UserManager()

class Secret(models.Model):
	content = models.TextField(max_length=500)
	created_at = models.DateTimeField(auto_now_add=True)
	users = models.ManyToManyField(User, related_name="secrets")
	created_by = models.ForeignKey(User, related_name="created")
	secretManager = SecretManager()
