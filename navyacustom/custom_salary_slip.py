from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from erpnext.payroll.doctype.salary_slip.salary_slip import SalarySlip

class CustomSalarySlip(SalarySlip):
    def calculate_total_for_salary_slip_based_on_timesheet(self):
        if self.timesheets:
            self.total_working_hours = 0
            for timesheet in self.timesheets:
                if timesheet.working_hours:
                    self.total_working_hours += timesheet.working_hours

        wages_amount = self.total_working_hours * self.hour_rate
        self.base_hour_rate = flt(self.hour_rate) * flt(self.exchange_rate)
        salary_component = frappe.db.get_value('Salary Structure', {'name': self.salary_structure}, 'salary_component')
        if self.earnings:
            for i, earning in enumerate(self.earnings):
                if earning.salary_component == salary_component:
                    self.earnings[i].amount = wages_amount
                self.gross_pay += self.earnings[i].amount
        self.net_pay = flt(self.gross_pay) - flt(self.total_deduction)