from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required()
def Dashboard(request):
	return render(request, 'users/dashboard.html', {})
