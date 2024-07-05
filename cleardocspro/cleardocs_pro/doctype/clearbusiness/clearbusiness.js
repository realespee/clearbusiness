// Copyright (c) 2024, Simon Wanyama and contributors
// For license information, please see license.txt

frappe.ui.form.on("ClearBusiness", {
	refresh(frm) {
        frm.trigger('filter_business_staff');
	},
    filter_business_staff(frm) {
        frm.fields_dict['business_staff'].grid.get_field('staff_name').get_query = function(doc, cdt, cdn) {
            return {
                filters: [
                    ['personnel_type', '=', 'Business Staff'],
                    ['business', '=', frm.doc.name]
                ]
            };
        };
    }
});

frappe.ui.form.on('ClearBusiness Staff', {
    staff_name(frm, cdt, cdn) {
        if(frappe.set_route('clearpersonnel/new-clearpersonnel')){
            frappe.route_options = {
				"personnel_type": 'Business Staff',
                "business": frm.doc.name
			};
            // return
        }
    },
    before_business_staff_remove(frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        // Deactivate the Business Staff with this staffname(name) from Personnel doctype
        if(row.staff_name){
            frappe.call({
                method: 'cleardocspro.cleardocs_pro.doctype.clearbusiness.clearbusiness.deactivate_personnel',
                args: {
                    'personnel': row.staff_name
                },
                callback: function(r) {
                    if(r.message) {
                        frappe.show_alert({
                            message: r.message
                        });
                    }
                    frm.save();
                }
            });
        }
    }
})

