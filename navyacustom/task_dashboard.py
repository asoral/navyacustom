from __future__ import unicode_literals
from frappe import _

def get_data(data):
	return {
		'fieldname': 'task',
		'transactions': [
			{
				'label': _('Activity'),
				'items': ['Timesheet', 'Drawing']
			},
			{
				'label': _('Accounting'),
				'items': ['Expense Claim']
			},
			{
				'label': _('Material Request'),
				'items': ['Material Request']
			}
		]
	}
