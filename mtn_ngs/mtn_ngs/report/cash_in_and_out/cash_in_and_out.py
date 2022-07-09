# Copyright (c) 2013, Trigger Solutions pvt. ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpnext.accounts.report.financial_statements import get_period_list
def execute(filters=None):
	columns, data = [], []
	period_list = get_period_list(filters.fiscal_year, filters.fiscal_year, '', '','Fiscal Year', filters.period)
	
	if filters.account:
		data=[{"name":filters.account}]
	else:
		data = get_account_type(filters.company)
	get_opening(data,period_list[0]["year_end_date"],filters.company)
	get_monthes(data,period_list,filters.company)
	columns = get_columns(period_list)
	return columns, data


def get_account_type(company):
	return( frappe.db.sql(f"""
		Select
			name
		from
			`tabAccount`
		where
			account_type in ("Cash","Bank")
		and 
			company = '{company}'	
	""", as_dict=1))

def get_opening(accounts,date,company):
	for account in accounts:
		opening = frappe.db.sql(f"""
						Select 
							COALESCE(SUM(debit)-SUM(credit), 0 ) as 'opening'
						from 
							`tabGL Entry` 
						where 
							account = '{account["name"]}'
						and 
							is_cancelled = 0
						and 
							company = '{company}'
						and 
							posting_date between '2000-01-01'
						and '{frappe.utils.add_days(date,-1)}';
					""", as_dict=1)
		account.update(opening[0])
	return accounts


def get_monthes(accounts,period_list,company):
	for account in accounts:
		for period in period_list:
			monthes = frappe.db.sql(f"""
							Select 
								COALESCE(SUM(debit), 0)  as '{period.key + "_debit"}'
							from 
								`tabGL Entry` 
							where 
								account = '{account["name"]}'
							and 
								is_cancelled = 0
							and 
								company = '{company}'
							and 
								posting_date between '{period['from_date']}'
							and '{period['to_date']}';
						""", as_dict=1)
			account.update(monthes[0])
		total_monthes = frappe.db.sql(f"""
				Select 
					COALESCE(SUM(debit), 0) as 'total_debit' 
				from 
					`tabGL Entry` 
				where 
					account = '{account["name"]}'
				and 
					is_cancelled = 0
				and 
					company = '{company}'
				and 
					posting_date between '{period_list[0]['year_start_date']}'
				and '{period_list[0]['year_end_date']}';
			""", as_dict=1)
		account.update(total_monthes[0])
		
	return accounts

def get_columns(period_list):
	columns = [
		{
			"fieldname": "name",
			"label": _("Account"),
			"fieldtype": "Link",
			"options": "Account",
			"width": 300
		},
		{
			"fieldname": "opening",
			"label": _("Opening Balance"),
			"fieldtype": "Currency",
			"width": 300,
			"options": "currency"
		}
	]

	for period in period_list:
		columns.append({
			"fieldname": period.key + "_debit",
			"label": period.label + "(Debit)",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150,
			'default': 0.0
		})
		# columns.append({
		# 	"fieldname": period.key +  "_credit",
		# 	"label": period.label +  "(Credit)",
		# 	"fieldtype": "Currency",
		# 	"options": "currency",
		# 	"width": 150,
		# 	'default': 0.0
		# })
		# columns.append({
		# 	"fieldname": period.key + "_balance",
		# 	"label": period.label + "(Balance)",
		# 	"fieldtype": "Currency",
		# 	"options": "currency",
		# 	"width": 150,
		# 	'default': 0.0
		# })
	
	columns.append({
			"fieldname":"total_debit",
			"label":"Total Debit",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150,
			'default': 0.0
		})
	# columns.append({
	# 	"fieldname":"total_credit",
	# 	"label": "Total Credit",
	# 	"fieldtype": "Currency",
	# 	"options": "currency",
	# 	"width": 150,
	# 	'default': 0.0
	# })
	# columns.append({
	# 	"fieldname": "total_balance",
	# 	"label": "Total Balance",
	# 	"fieldtype": "Currency",
	# 	"options": "currency",
	# 	"width": 150,
	# 	'default': 0.0
	# })

	return columns


