from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import *

app_name = 'users'

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name="homepage.html", redirect_authenticated_user=True) \
    	, name="homepage"),
]