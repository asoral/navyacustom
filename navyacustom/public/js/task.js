frappe.ui.form.on("Task", {
    refresh: function(frm){
        if(!frm.doc.__islocal){
            frm.add_custom_button(__('Material Request'), function() {
					frm.trigger('make_material_request');
				}, __('Create'));
        }
    },
    make_material_request: function(frm) {
		frappe.call({
			args: {
				'task': frm.doc.name,
				'project': frm.doc.project,
				'company': frm.doc.company
			},
			method: 'navyacustom.custom_task.make_material_request',
			callback: function(r) {
				var doclist = frappe.model.sync(r.message);
				frappe.set_route('Form', doclist[0].doctype, doclist[0].name);
			}
		});
	}
});