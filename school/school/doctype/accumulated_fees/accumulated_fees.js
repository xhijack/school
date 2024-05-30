// Copyright (c) 2024, PT Sopwer Teknologi Indonesia and contributors
// For license information, please see license.txt

frappe.ui.form.on("Accumulated Fees", {
	refresh(frm) {
        frm.set_query("fee_structure", function() {
            return {
                filters: {
                    student: frm.doc.student
                }
            };
        });
	},
});

frappe.ui.form.on("Accumulated Fees Detail", {
    priod: function(frm, cdt, cdn){
        var row = locals[cdt][cdn];
        console.log(row);
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: 'Fee Structure',
                filters: {
                    fee_structure: row.fee_structure
                },
                fieldname: ['total']
            },
            callback: function (r) {
                if (r.message) {
                    console.log(r.message); 
                    frappe.model.set_value(row.doctype, row.name, 'amount', r.message.total);
                }
            }
        })
    }
});