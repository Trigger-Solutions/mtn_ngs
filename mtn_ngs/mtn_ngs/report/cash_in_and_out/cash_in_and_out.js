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
		{
			fieldname: "account",
			label: __("Account"),
			fieldtype: "Link",
			options: "Account",
			"get_query": function(){ return {'filters': [['company','=',frappe.query_report.get_filter_value("company")],
			['account_type','in',["Cash","Bank"]]]}}
		},
		{
			fieldname: "period",
			label: __("Period"),
			fieldtype: "Select",
			options: [
				{ "value": "Yearly", "label": __("Yearly") },
				{ "value": "Quarterly", "label": __("Quarterly" ) },
				{ "value": "Monthly", "label": __("Monthly" ) },
			],
			default: "Yearly",
			reqd:1
			// depends_on: 'eval:doc.company=="Gadget Technologies Pvt. Ltd."'
		},
	]
}
