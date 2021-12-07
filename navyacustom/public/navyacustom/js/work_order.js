frappe.ui.form.on("Work Order", {
    refresh: function(frm){
        var doc = frm.doc;
        if(frm.doc.pattern){
		    if (doc.docstatus === 1) {
                const show_start_btn = (frm.doc.skip_transfer || frm.doc.transfer_material_against == 'Job Card') ? 0 : 1;

                if (show_start_btn) {
                    if ((flt(doc.material_transferred_for_manufacturing) < flt(doc.qty))
                        && frm.doc.status != 'Stopped') {
                        frm.add_custom_button(__('Make Asset Movement'), function() {
                            frappe.call({
                                method: "navyacustom.custom_work_order.make_asset_movement",
                                args: {
                                    work_order: frm.doc.name,
                                    purpose: 'Material Transfer for Manufacture',
                                },
                                callback: function(r) {
                                    if(r.message) {
                                        var doclist = frappe.model.sync(r.message);
                                        frappe.set_route('Form',doclist[0].doctype, doclist[0].name);
                                    }
                                }
                            });
                        });
                    }
                }

                if(!frm.doc.skip_transfer){
                    // If "Material Consumption is check in Manufacturing Settings, allow Material Consumption
                    if ((flt(doc.produced_qty) < flt(doc.material_transferred_for_manufacturing))
                    && frm.doc.status != 'Stopped') {
                        frm.add_custom_button(__('Make Asset Movement'), function() {
                            frappe.call({
                                method: "navyacustom.custom_work_order.make_asset_movement",
                                args: {
                                    work_order: frm.doc.name,
                                    purpose: 'Manufacture',
                                },
                                callback: function(r) {
                                    if(r.message) {
                                        var doclist = frappe.model.sync(r.message);
                                        frappe.set_route('Form',doclist[0].doctype, doclist[0].name);
                                    }
                                }
                            });
                        });
                    }
                }
                else {
                    if ((flt(doc.produced_qty) < flt(doc.qty)) && frm.doc.status != 'Stopped')
                    {
                        frm.add_custom_button(__('Make Asset Movement'), function() {
                            frappe.call({
                                method: "navyacustom.custom_work_order.make_asset_movement",
                                args: {
                                    work_order: frm.doc.name,
                                    purpose: 'Manufacture',
                                },
                                callback: function(r) {
                                    if(r.message) {
                                        var doclist = frappe.model.sync(r.message);
                                        frappe.set_route('Form',doclist[0].doctype, doclist[0].name);
                                    }
                                }
                            });
                        });
                    }
                }
            }
		}
    }
});