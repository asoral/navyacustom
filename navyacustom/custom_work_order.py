

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt
from datetime import datetime

@frappe.whitelist()
def make_stock_entry(work_order_id, purpose, qty=None):
    work_order = frappe.get_doc("Work Order", work_order_id)
    # make_asset_movement(work_order, purpose)
    if purpose =='Manufacture':
        make_employee_time_sheet(work_order)

    if not frappe.db.get_value("Warehouse", work_order.wip_warehouse, "is_group"):
        wip_warehouse = work_order.wip_warehouse
    else:
        wip_warehouse = None

    stock_entry = frappe.new_doc("Stock Entry")
    stock_entry.purpose = purpose
    stock_entry.work_order = work_order_id
    stock_entry.company = work_order.company
    stock_entry.from_bom = 1
    stock_entry.bom_no = work_order.bom_no
    stock_entry.use_multi_level_bom = work_order.use_multi_level_bom
    stock_entry.fg_completed_qty = qty or (flt(work_order.qty) - flt(work_order.produced_qty))
    if work_order.bom_no:
        stock_entry.inspection_required = frappe.db.get_value('BOM',
            work_order.bom_no, 'inspection_required')

    if purpose=="Material Transfer for Manufacture":
        stock_entry.to_warehouse = wip_warehouse
        stock_entry.project = work_order.project
    else:
        stock_entry.from_warehouse = wip_warehouse
        stock_entry.to_warehouse = work_order.fg_warehouse
        stock_entry.project = work_order.project

    stock_entry.set_stock_entry_type()
    stock_entry.get_items()
    return stock_entry.as_dict()

@frappe.whitelist()
def make_asset_movement(work_order, purpose):
    work_order = frappe.get_doc("Work Order",work_order)
    if work_order.pattern:
        asset = frappe.get_doc('Asset', work_order.pattern)
        if asset:
            asset_movement = frappe.new_doc("Asset Movement")
            asset_movement.transaction_date = datetime.now()
            asset_movement.company = work_order.company
            asset_movement.work_order = work_order.name
            if purpose == "Material Transfer for Manufacture":
                asset_movement.purpose = "Issue"
                asset_movement.append("assets", {
                    'asset': asset.name,
                    'source_location': asset.location,
                    'from_employee': asset.custodian
                })
            else:
                if not work_order.location:
                    frappe.throw("Select the Location for Asset Movement!")
                asset_movement.purpose = "Receipt"
                asset_movement.append("assets", {
                    'asset': asset.name,
                    'source_location': asset.location,
                    'target_location': work_order.location,
                    'from_employee': asset.custodian
                })
            # asset_movement.insert(ignore_permissions=True)
            # asset_movement.flags.ignore_validate_update_after_submit = True
            # asset_movement.submit()
            return asset_movement.as_dict()
        return False

def make_employee_time_sheet(work_order):
    if work_order:
        job_cards = frappe.get_list("Job Card", filters={"work_order": work_order.name})
        job_list = []
        for job_c in job_cards:
            job_list.append(job_c.name)
        if job_list:
            employee_job = frappe.db.sql("""select distinct employee from `tabJob Card`
                            where name in {0}""".format(tuple(job_list)), as_dict=True)
            for emp in employee_job:
                job_dates = frappe.db.sql("""select distinct tc.employee, tct.from_time,tct.to_time from `tabJob Card` as tc
                            inner join `tabJob Card Time Log` as tct on tct.parent = tc.name
                            where tc.name in {0} and tc.employee = '{1}' and tc.docstatus = 1 
                            and tct.from_time is not null and tct.to_time is not null
                            order by tc.employee""".format(tuple(job_list), emp.employee), as_dict=True)
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
                            t_sheet.employee = emp.employee
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
