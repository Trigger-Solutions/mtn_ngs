# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt


from functools import total_ordering
import frappe
from frappe import _
from erpnext.accounts.report.financial_statements import get_period_list
import collections
from console import console

def execute(filters=None):
	period_list = get_period_list(filters.fiscal_year, filters.fiscal_year, '', '','Fiscal Year', "Monthly")
	columns,data = [],[]
	all_data = get_account_type()
	all_data = get_opening(all_data,period_list[0]["year_end_date"])
	all_data = get_monthes(all_data,period_list)
	console(all_data).log()
	columns = get_columns(period_list)
	data = all_data

	return columns, data





def get_data():
	pass


def get_account_type():
	return( frappe.db.sql(f"""
		Select
			name
		from
			`tabAccount`
		where
			account_type in ("Cash","Bank")
	""", as_dict=1))


def get_opening(accounts,date):
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
							posting_date between '2000-01-01'
						and '{frappe.utils.add_days(date,-1)}';
					""", as_dict=1)
		account.update(opening[0])
	return accounts

def get_monthes(accounts,period_list):
	for account in accounts:
		for period in period_list:
			monthes = frappe.db.sql(f"""
							Select 
								COALESCE(SUM(debit), 0)  as '{period.key + "_debit"}' ,
								COALESCE(SUM(credit), 0)  as '{period.key + "_credit"}' ,
								COALESCE(SUM(debit)-SUM(credit), 0 ) as '{period.key + "_balance"}' 
							from 
								`tabGL Entry` 
							where 
								account = '{account.name}'
							and 
								is_cancelled = 0
							and 
								posting_date between '{period['from_date']}'
							and '{period['to_date']}';
						""", as_dict=1)
			account.update(monthes[0])
		total_monthes = frappe.db.sql(f"""
				Select 
					COALESCE(SUM(debit), 0) as 'total_debit' ,
					COALESCE(SUM(credit), 0) as 'total_credit' ,
					COALESCE(SUM(debit)-SUM(credit), 0 ) as 'total_balance' 
				from 
					`tabGL Entry` 
				where 
					account = '{account.name}'
				and 
					is_cancelled = 0
				and 
					posting_date between '{period['year_start_date']}'
				and '{period['year_end_date']}';
			""", as_dict=1)
		accounts.append(total_monthes[0])
		
	return accounts

def get_columns(period_list):
	columns = [
		{
			"fieldname": "account",
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
		columns.append({
			"fieldname": period.key +  "total_credit",
			"label": period.label +  "(Credit)",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150,
			'default': 0.0
		})
		columns.append({
			"fieldname": period.key + "_balance",
			"label": period.label + "(Balance)",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150,
			'default': 0.0
		})
	
	columns.append({
			"fieldname":"total_debit",
			"label":"Total Debit",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150,
			'default': 0.0
		})
	columns.append({
		"fieldname":"total_credit",
		"label": "Total Credit",
		"fieldtype": "Currency",
		"options": "currency",
		"width": 150,
		'default': 0.0
	})
	columns.append({
		"fieldname": "total_balance",
		"label": "Total Balance",
		"fieldtype": "Currency",
		"options": "currency",
		"width": 150,
		'default': 0.0
	})

	return columns