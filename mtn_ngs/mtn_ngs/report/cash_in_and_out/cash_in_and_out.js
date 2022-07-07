// Copyright (c) 2016, Trigger Solutions pvt. ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.query_reports["Cash In and Out"] = {
	"filters": [
		{
			fieldname: "fiscal_year",
			label: __("Fiscal Year"),
			fieldtype: "Link",
			options: "Fiscal Year",
			default: frappe.sys_defaults.fiscal_year,
			reqd:1
		},
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd:1
		},
	]
}
