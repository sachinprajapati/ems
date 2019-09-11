from collections import namedtuple
from ems.settings import conn

cur = conn.cursor()

def getFlatDetail(tower, flat):
	flatt = namedtuple('Flat',['sno','flat_pkey','flat_no', 'tower_no', 'flat_size', 'owner', \
	 'prof', 'status', 'mob', 'email', 'meter_no', 'flat_basis', 'fixed_amt', 'field_name', 'field_amt']) 
	flat = cur.execute("select * from TblFlat where Tower_No="+tower+" and Flat_No="+flat)
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