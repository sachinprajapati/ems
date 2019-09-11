from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import *

app_name = 'users'

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name="homepage.html", redirect_authenticated_user=True) \
    	, name="homepage"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('dashboard/', Dashboard, name="dashboard"),
    path('recharge/', Recharge, name="recharge"),
    path('bill/', getBill, name="bill"),
    path('bill-report/', genrateBill, name="bill"),
    path('recharge-history/', RechargeHistory, name="recharge_history"),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name="users/change_password.html"), name="change_password"),
    path('recharge-list/', RechargeList, name="recharge_list"),
    path('recharge-success/', RechargeSuccess, name="recharge_success"),
    path("getFlat/", getFlat, name="getFlat"),
]