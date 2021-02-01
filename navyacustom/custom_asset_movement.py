
from __future__ import unicode_literals
import frappe
from frappe import _
from erpnext.assets.doctype.asset_movement.asset_movement import AssetMovement

class CustomAssetMovement(AssetMovement):
    def set_latest_location_in_asset(self):
        current_location, current_employee = '', ''
        cond = "1=1"

        for d in self.assets:
            args = {
                'asset': d.asset,
                'company': self.company
            }

            # latest entry corresponds to current document's location, employee when transaction date > previous dates
            # In case of cancellation it corresponds to previous latest document's location, employee
            latest_movement_entry = frappe.db.sql(
                """
                SELECT asm_item.target_location, asm_item.to_employee 
                FROM `tabAsset Movement Item` asm_item, `tabAsset Movement` asm
                WHERE 
                    asm_item.parent=asm.name and
                    asm_item.asset=%(asset)s and
                    asm.company=%(company)s and 
                    asm.docstatus=1 and {0}
                ORDER BY
                    asm.transaction_date desc limit 1
                """.format(cond), args)
            if latest_movement_entry:
                current_location = latest_movement_entry[0][0]
                current_employee = latest_movement_entry[0][1]

                frappe.db.set_value('Asset', d.asset, 'location', current_location)
                frappe.db.set_value('Asset', d.asset, 'custodian', current_employee)
