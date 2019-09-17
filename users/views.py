from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from django.db import transaction

from collections import OrderedDict
from itertools import chain
from ems.settings import conn

from .functions import *
from .forms import *
from .models import Recharge

import time
from datetime import datetime

import pytz

cur = conn.cursor()


def convert_to_localtime(utctime):
	fmt = '%d/%m/%Y %H:%M'
	utc = utctime.replace(tzinfo=pytz.UTC)
	localtz = pytz.timezone("Asia/Calcutta")
	localtz = utc.astimezone(localtz)
	return localtz

@login_required()
def Dashboard(request):
	return render(request, 'users/dashboard.html', {})


@login_required()
def Recharge(request):
	context = {}
	errors = []
	if request.method == "POST":
		data = request.POST
		try:
			with transaction.atomic():
				if data.get("id") and data.get("tower") and data.get("flat") and data.get("recharge-amt") \
					and data.get("type"):
					dt = convert_to_localtime(timezone.now())

					if data["type"] == "Bank" and data.get("chq"):
						chq_dd = data["chq"]
					else:
						chq_dd = None
					bal = getBalanceReport(data["id"])
					recharge_no = getCurrentsr()
					print(dt.strftime("%d/%m/%y %H:%M %p"))
					formdata = {"flat": data["id"], "amount": data["recharge-amt"]}
					form = RechargeForm(formdata)
					if form.is_valid():
						form.save()
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
					return render(request, "users/recharge_success.html", context)
		except Exception as e:
			errors.append(e)
	context = {"errors" : errors}
	return render(request, 'users/recharge.html', context)

@login_required()
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

@login_required()
def getBill(request):
	context = {}
	if request.method == "POST":
		data = request.POST
		if data.get('id') and data.get('month'):
			date = datetime.strptime(data['month'], "%Y-%m").date()
			print("month is ", date)
			mf = getMaintanceFixed(data['id'], date)
			print(mf)
			bill = getMonthlyBill(data['id'], date)
			context = {
				"bill": bill,
				"mf": mf,
				"date": date,
				"flat": getFlatDetailByKey(data["id"])
			}
			return render(request, 'users/bill_report.html', context)
	return render(request, 'users/getBill.html', context)


@login_required()
def DailyRechargeReport(request):
	context = {
		"args": {"type": "date", "name": "date"}
	}
	if request.method == "POST":
		date = request.POST.get("date", "")
		print("date is ", date)
		if date:
			try:
				date = datetime.strptime(date, "%Y-%m-%d").date()
				sql = "select * from [TblRecharge] where recharge_date between '{0}' and '{0} 23:59:59'".format(date.strftime("%Y/%m/%d"))
				recharge, total = getRechargeHistory(sql)
				context = {
				"recharge": recharge,
				"total": total,
				}
			except Exception as e:
				print(e)
	return render(request, 'users/rechargehistory.html', context)


@login_required()
def MonthlyRechargeReport(request):
	context = {
		"args": {"type": "month", "name": "month"}
	}
	if request.method == "POST":
		date = request.POST.get("month", "")
		print("month is ", date)
		if date:
			try:
				date = datetime.strptime(date, "%Y-%m").date()
				print(date)
				sql = "SELECT * FROM TblRecharge WHERE MONTH(recharge_date) = {} AND YEAR(recharge_date) = {}".format(date.month, date.year)
				print("sql is ",sql)
				recharge, total = getRechargeHistory(sql)
				context = {
				"recharge": recharge,
				"total": total,
				}
			except Exception as e:
				print(e)
	return render(request, 'users/rechargehistory.html', context)


@login_required()
def FlatRechargeReport(request):
	context = {
		"args": {"type": "month", "name": "month"},
		"flatrecharge": True,
	}
	if request.method == "POST":
		flat_pkey = request.POST.get("id", "")
		print("flat_pkey is ", flat_pkey)
		if flat_pkey:
			try:
				sql = "SELECT * FROM TblRecharge WHERE flat_pkey={}".format(flat_pkey)
				print("sql is ",sql)
				recharge, total = getRechargeHistory(sql)
				context = {
				"recharge": recharge,
				"total": total,
				}
			except Exception as e:
				print(e)
	return render(request, 'users/rechargehistory.html', context)

@login_required()
def NegativeBalanceFlats(request):
	context = {
		"flats": getNegativeFlats,
	}
	return render(request, 'users/negative-flats.html', context)

@login_required()
def RechargeList(request):
	return render(request, 'users/recharge_list.html', {})

@login_required()
def genrateBill(request):
	return render(request, 'users/bill_report.html', {})

@login_required()
def RechargeSuccess(request):
	return render(request, 'users/recharge_success.html', {})
