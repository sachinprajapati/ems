from django.db import models
from django.contrib.auth.models import User


class Type(models.Model):
	name = models.CharField(max_length=55, unique=True)

class UserType(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	Type = models.ForeignKey(Type, on_delete=models.CASCADE)

class Recharge(models.Model):
	flat = models.PositiveIntegerField()
	amount = models.PositiveIntegerField()
	datetime = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return "{} {} at {}".format(self.flat, self.amount, self.datetime.strftime("%d/%m/%y %H:%M %p"))