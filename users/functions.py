from collections import namedtuple
from ems.settings import conn

cur = conn.cursor()

def getFlatDetail(tower, flat):
	flatt = namedtuple('Flat',['sno','flat_pkey','flat_no', 'tower_no', 'flat_size', 'owner', \
	 'prof', 'status', 'mob', 'email', 'meter_no', 'flat_basis', 'fixed_amt', 'field_name', 'field_amt']) 
	sql = "select * from TblFlat where Tower_No="+tower+" and Flat_No="+flat
	print("sql is ", sql)
	try:
		flat = cur.execute(sql)
	except Exception as e:
		print(e)
	else:
		a = flat.fetchone()
		if a:
			a = flatt(*a)
		return a

def getFlatDetailByKey(flat_pkey):
	flatt = namedtuple('Flat',['sno','flat_pkey','flat_no', 'tower_no', 'flat_size', 'owner', \
	 'prof', 'status', 'mob', 'email', 'meter_no', 'flat_basis', 'fixed_amt', 'field_name', 'field_amt']) 
	flat = cur.execute("select * from TblFlat where flat_pkey="+flat_pkey)
	a = flat.fetchone()
	if a:
		a = flatt(*a)
	return a


def getBalanceReport(flat_pkey):
	# Consumption = namedtuple('Consumption',['sno','date','flat_pkey', 'tower_no', 'flat_no', 'utility_kwh', \
	#  'dg_kwh', 'ref_utility_kwh', 'ref_dg_kwh', 'amt_left', 'recharge_amt', 'start_utility_kwh', 'start_dg_kwh', \
	#   'status', 'msg_status', 'reset_date', 'meter_change_date', 'row', 'sim_msg_status', 'last_modify' \
	#   'last_deduction_date', 'deduction', 'negative_utility', 'negative_dg_kwh', 'negative_date'])
	Consumption = namedtuple('Consumption', ["SNo","Date","Flat_Pkey","Tower_No","Flat_No","Utility_KWH","DG_KWH",\
		"Ref_Utility_KWH","Ref_DG_KWH","Amt_Left","Recharge_Amt","Start_Utility_KWH","Start_DG_KWH","Status",\
		"Msg_Status","Reset_Date","Meter_Change_Date","RowVersion","SIM_Msg_Status","Last_Modified","Last_Deduction_Date",\
		"Deduction_YN","Negative_Utility_KWH","Negative_DG_KWH","Negative_Date"])
	a = cur.execute("SELECT * FROM TblConsumption where flat_Pkey=?",[flat_pkey])
	data = a.fetchone()
	cons = Consumption(*data)
	return cons

def getCurrentsr():
	a = cur.execute("select TOP 1 recharge_no from TblRecharge order by sno desc")
	b = a.fetchone()
	return int(b[0]+1)

def getRechargeHistory(sql):
	Recharge = namedtuple("Recharge", ["SNo","Recharge_No","Recharge_Date","Flat_Pkey","Amount_Left", \
		"Recharge_Amt","Rpt_TYPE","RPT_Chq_DD","Chq_DD_No","Chq_DD_Date","UsrName","Recharge_TYPE","Utility_KWH","DG_KWH"])
	a = cur.execute(sql)
	data = a.fetchall()
	recharge = []
	total = 0
	for i in data:
		r = Recharge(*i)
		recharge.append(r)
		total += r.Recharge_Amt
	return recharge, total


def getNegativeFlats():
	NegativeFlats = namedtuple("NegativeFlats", ["tower_no", "flat_no", "owner", "mob", "amt_left"])
	sql = "SELECT TblConsumption.tower_no, TblConsumption.flat_no, TblFlat.Owner, TblFlat.mobile_no, TblConsumption.amt_left \
			FROM [TblConsumption] INNER JOIN TblFlat ON TblConsumption.flat_pkey = TblFlat.flat_pkey \
			where TblConsumption.amt_left < 0 ORDER BY TblConsumption.tower_no, TblConsumption.flat_no;"
	a = cur.execute(sql)
	ls = []
	if a:
		for i in a:
			ls.append(NegativeFlats(*i))
	return ls

def getMonthlyBill(flat_pkey, month):
	MonthlyBill = namedtuple("MonthlyBill", ["Bill_Pkey","Flat_Pkey","Month","Year","Start_EB","Start_DG", \
		"End_EB","End_DG","Opening_Amt","Closing_Amt","Utility_Rate","DG_Rate","Inserted_Date","Updated_Date"])
	sql = "SELECT * from [TblMonthlyBill] where flat_pkey={} and year={} and month={}".format(flat_pkey, month.year, month.month)
	a = cur.execute(sql)
	m = MonthlyBill(*a.fetchone())
	if m:
		consume = {}
		consume['ebconsume'] = m.End_EB - m.Start_EB
		consume['dgconsume'] = m.End_DG - m.Start_DG
		consume['ebprice'] = consume['ebconsume'] * m.Utility_Rate
		consume['dgprice'] = consume['dgconsume'] * m.DG_Rate
	return m, consume


def getMaintanceFixed(flat_pkey, month):
	MaintanceFixed = namedtuple("MaintanceFixed", ["maintance", "fixed"])
	sql = "SELECT sum(Maintenance_charges) as maintance, sum([Fixed_Amt]) as fixed from [TblMaintenance] \
		where flat_pkey={} and month(Date) = {} and year(Date) = {}".format(flat_pkey, month.month, month.year)
	print(sql)
	a = cur.execute(sql)
	if a:
		return MaintanceFixed(*a.fetchone())
	return MaintanceFixed((0,0))


def rechargeInMonth(flat_pkey, date):
	sql = "select sum(recharge_amt) from [TblRecharge] where flat_pkey={} and month(recharge_date)={} \
	and year(recharge_date)={}".format(flat_pkey, date.month, date.year)
	r = cur.execute(sql)
	r = r.fetchone()
	if not r:
		r = 0
	else:
		r = r[0]
	return r
