from django.db import models

class Profile(models.Model):
	username=models.CharField(max_length=30)
	phoneNumber = models.CharField(max_length=20)
	email = models.EmailField(max_length=50)
	user = models.CharField(max_length=60)
