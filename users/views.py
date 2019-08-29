from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required()
def Dashboard(request):
	return render(request, 'users/dashboard.html', {})


@login_required
def Recharge(request):
	return render(request, 'users/recharge.html', {})

@login_required
def getBill(request):
	return render(request, 'users/getBill.html', {})


@login_required
def RechargeHistory(request):
	return render(request, 'users/rechargehistory.html', {})

@login_required
def RechargeList(request):
	return render(request, 'users/recharge_list.html', {})
