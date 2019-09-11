from django.db import models
from django.contrib.auth.models import User


class Type(models.Model):
	name = models.CharField(max_length=55, unique=True)

class UserType(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	Type = models.ForeignKey(Type, on_delete=models.CASCADE)
