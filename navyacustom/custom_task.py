from __future__ import unicode_literals
import frappe

@frappe.whitelist()
def make_material_request(task, project=None, company=None):
    m_request = frappe.new_doc("Material Request")
    m_request.task = task
    m_request.company = company
    item_name = ''
    uom = ''
    items = frappe.get_list('Item',filters=[['name', 'in', 'Custom Product Request']],limit=1)
    if not items:
        item = frappe.new_doc("Item")
        item.item_name = 'Custom Product Request'
        item.item_code = 'Custom Product Request'
        item.item_group = 'All Item Groups'
        item.stock_uom = 'Nos'
        item.standard_rate = 0
        item.insert()
        item_name = item.name
        uom = item.stock_uom
    else:
        item = frappe.get_doc("Item",items[0].name)
        item_name = item.name
        uom = item.stock_uom

    m_request.append("items", {
        "item_code": item_name,
        "qty": 1,
        "uom": uom,
        "project": project,
    })
    return m_request

def set_expected_time_in_job_card(obj,method):
    if obj.operation_id:
        query = frappe.db.sql("""select * from `tabWork Order Operation` where name = %s limit 1""",(obj.operation_id), as_dict= True)
        if query:
            if query[0].time_in_mins:
                obj.expected_time = query[0].time_in_mins
                obj.db_update()