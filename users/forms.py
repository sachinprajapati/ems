from django.forms import ModelForm
from .models import Recharge


class RechargeForm(ModelForm):
	class Meta:
		model = Recharge
		fields = ['flat', "amount"]