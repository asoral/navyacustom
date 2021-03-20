from __future__ import unicode_literals
import frappe
from datetime import datetime



def make_employee_time_sheet(job_card, method):
    if job_card:
        if job_card.employee:
            job_dates = frappe.db.sql("""select distinct tc.employee, tct.from_time,tct.to_time from `tabJob Card` as tc
                        inner join `tabJob Card Time Log` as tct on tct.parent = tc.name
                        where tc.name = '{0}' and tc.employee = '{1}' and tc.docstatus = 1 
                        and tct.from_time is not null and tct.to_time is not null
                        order by tc.employee""".format(job_card.name, job_card.employee), as_dict=True)
            for j_date in job_dates:
                timesheet = frappe.db.sql("""select tc.employee, tcd.from_time, tcd.to_time from `tabTimesheet Detail` as tcd
                            inner join `tabTimesheet` as tc on tc.name = tcd.parent
                            where tc.employee = %s 
                            and tcd.from_time between %s and %s 
                            or tcd.to_time between  %s and %s""", (j_date.employee, str(j_date.from_time),
                                                                   str(j_date.to_time), str(j_date.from_time), str(j_date.to_time)))
                if not timesheet:
                    try:
                        from_date = datetime.strptime((str(j_date.from_time)[:-2]+"00"), '%Y-%m-%d %H:%M:%S')
                        to_date = datetime.strptime((str(j_date.to_time)[:-2]+"00"), '%Y-%m-%d %H:%M:%S')
                        t_sheet = frappe.new_doc("Timesheet")
                        t_sheet.employee = job_card.employee
                        t_sheet.work_order = job_card.work_order
                        t_sheet.job_card = job_card.name
                        date_diff = (to_date - from_date).seconds
                        date_diff = date_diff / 3600
                        t_sheet.append("time_logs", {
                            "activity_type": "Execution",
                            "from_time": from_date,
                            "to_time": to_date,
                            "hours": round(date_diff,3),
                            "hrs": round(date_diff,3)
                        })
                        t_sheet.insert(ignore_permissions=True)
                        t_sheet.validate()
                    except Exception as e:
                        print("-------------e",e)
                        pass
