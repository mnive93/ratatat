from django.db import models

class SignupHandler(models.Model):
	emailaddress = models.EmailField(max_length=200)
	identifiernum = models.IntegerField()
