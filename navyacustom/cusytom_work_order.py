

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt
from datetime import datetime

@frappe.whitelist()
def make_stock_entry(work_order_id, purpose, qty=None):
    work_order = frappe.get_doc("Work Order", work_order_id)

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
                    'to_employee': asset.custodian
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
            asset_movement.insert(ignore_permissions=True)
            asset_movement.flags.ignore_validate_update_after_submit = True
            asset_movement.submit()

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