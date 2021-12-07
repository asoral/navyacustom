# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "navyacustom"
app_title = "NavyaCustom"
app_publisher = "Dexciss"
app_description = "NavyaCustom"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "support@dexciss.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/navyacustom/css/custom_css.css"
# app_include_js = "/assets/navyacustom/js/navyacustom.js"

# include js, css files in header of web template
# web_include_css = "/assets/navyacustom/css/navyacustom.css"
# web_include_js = "/assets/navyacustom/js/navyacustom.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "navyacustom/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Task": "public/js/task.js",
	"Work Order": "public/js/work_order.js",
        #"Item":"public/js/image_view.js",
}
doctype_list_js = {

        "Item":"public/navyacustom/js/image_view.js",
        "Project":"public/navyacustom/js/image_view.js",
        "Image View":"public/navyacustom/js/image_view.js"


        }

# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------
fixtures = ['Custom Field', 'Property Setter', 'Workflow', 'Workflow State', 'Workflow Action']

# before_install = "navyacustom.install.before_install"
# after_install = "navyacustom.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "navyacustom.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Salary Slip": "navyacustom.custom_salary_slip.CustomSalarySlip",
	"Asset Movement": "navyacustom.custom_asset_movement.CustomAssetMovement"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Job Card": {
		"after_insert": "navyacustom.custom_task.set_expected_time_in_job_card",
		"on_submit": "navyacustom.custom_job_card.make_employee_time_sheet"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"navyacustom.tasks.all"
# 	],
# 	"daily": [
# 		"navyacustom.tasks.daily"
# 	],
# 	"hourly": [
# 		"navyacustom.tasks.hourly"
# 	],
# 	"weekly": [
# 		"navyacustom.tasks.weekly"
# 	]
# 	"monthly": [
# 		"navyacustom.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "navyacustom.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"erpnext.manufacturing.doctype.work_order.work_order.make_stock_entry": "navyacustom.custom_work_order.make_stock_entry"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
override_doctype_dashboards = {
	"Task": "navyacustom.task_dashboard.get_data",
	"Work Order": "navyacustom.word_order_dashboard.get_data",
	"Job Card": "navyacustom.job_card_dashboard.get_data"
}

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

