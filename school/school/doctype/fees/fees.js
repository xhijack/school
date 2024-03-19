// Copyright (c) 2024, PT Sopwer Teknologi Indonesia and contributors
// For license information, please see license.txt

frappe.ui.form.on("Fees", {
	refresh(frm) {
        // Set default Fee Structure based on selected student
        frm.set_query("fee_structure", function() {
            return {
                filters: {
                    student: frm.doc.student
                }
            };
        });
	},
    fee_structure(frm) {
        // Get Fee Structure details
        if (frm.doc.fee_structure) {
            frappe.call({
                method: "school.school.doctype.fees.fees.get_fee_structure_details",
                args: {
                    fee_structure: frm.doc.fee_structure
                },
                callback: function(r) {
                    if (r.message) {
                        frm.doc.fees_detail = r.message;
                        frm.refresh_field("fees_detail");
                    }
                }
            });
        }
    }
});
