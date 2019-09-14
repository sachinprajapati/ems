from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings

from collections import OrderedDict
from itertools import chain
from ems.settings import conn

from .functions import *
from .forms import *

import time
from datetime import datetime

import pytz

cur = conn.cursor()


def convert_to_localtime(utctime):
	fmt = '%d/%m/%Y %H:%M'
	utc = utctime.replace(tzinfo=pytz.UTC)
	localtz = utc.astimezone(timezone.get_current_timezone())
	return localtz

@login_required()
def Dashboard(request):
	return render(request, 'users/dashboard.html', {})


@login_required
def Recharge(request):
	if request.method == "POST":
		data = request.POST
		if data.get("id") and data.get("tower") and data.get("flat") and data.get("recharge-amt") \
			and data.get("type"):
			dt = convert_to_localtime(timezone.now())

			if data["type"] == "Bank" and data.get("chq"):
				chq_dd = data["chq"]
			else:
				chq_dd = None
			bal = getBalanceReport(data["id"])
			recharge_no = getCurrentsr()
			sql = "INSERT INTO [TblRecharge] ([Recharge_No] ,[Recharge_Date] ,[Flat_Pkey] ,[Amount_Left] ,[Recharge_Amt] \
				,[Rpt_TYPE] ,[RPT_Chq_DD] ,[Chq_DD_No] ,[Chq_DD_Date] ,[UsrName] ,[Recharge_TYPE] ,[Utility_KWH],[DG_KWH]) \
				VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"
			cur.execute(sql, [recharge_no, dt, data["id"], bal.Amt_Left, data["recharge-amt"], data["type"] ,1, chq_dd, dt, "cashier", \
				"R", bal.Utility_KWH, bal.DG_KWH])
			sql1 = "UPDATE [TblConsumption] set [amt_left]=? where flat_pkey=?"
			total = bal.Amt_Left+int(data['recharge-amt'])
			cur.execute(sql1, [total, data["id"]])
			conn.commit()
			context = {
			"data": getFlatDetailByKey(data["id"]),
			"bal": bal,
			'recharge_amt' : data['recharge-amt'],
			"total" : total
			}
			print(context)
			return render(request, "users/recharge_success.html", context)
		else:
			return HttpResponse("fail")
	return render(request, 'users/recharge.html', {})

@login_required
def getFlat(request):
	if request.method == "POST":
		tower = request.POST.get("tower", '')
		flat = request.POST.get("flat", '')
		if tower and flat:
			flat = getFlatDetail(tower, flat)
			if flat:
				a = flat._asdict()
				b = dict(getBalanceReport(flat.flat_pkey)._asdict())
				a['Amt_Left'] = b['Amt_Left']
				a['Utility_KWH'] = b['Utility_KWH']
				a['DG_KWH'] = b['DG_KWH']
				return JsonResponse(a)
	return HttpResponse(status=404)

@login_required
def getBill(request):
	if request.method == "POST":
		data = request.POST
		if data.get('id') and data.get('month'):
			bill = getMonthlyBill(data['id'], data['month'])
			print(bill)
	return render(request, 'users/getBill.html', {})


@login_required
def RechargeHistory(request):
	context = {}
	if request.method == "POST":
		date = request.POST.get("date", "")
		if date:
			try:
				date = datetime.strptime(date, "%Y-%m-%d").date()
				recharge, total = getRechargeHistory(date)
				context = {
				"recharge": recharge,
				"total": total,
				}
			except Exception as e:
				print(e)
	return render(request, 'users/rechargehistory.html', context)

@login_required
def RechargeList(request):
	return render(request, 'users/recharge_list.html', {})

@login_required
def genrateBill(request):
	return render(request, 'users/bill_report.html', {})

@login_required
def RechargeSuccess(request):
	return render(request, 'users/recharge_success.html', {})
