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

        // Add Pay button if status is unpaid
        if (frm.doc.status === "Unpaid") {
            frm.add_custom_button(__('Pay'), function() {
                // Open dialog for payment details
                frappe.prompt([
                    {
                        fieldname: 'attachment',
                        fieldtype: 'Attach',
                        label: 'Attachment'
                    },
                    {
                        fieldname: 'transfer_date',
                        fieldtype: 'Date',
                        label: 'Transfer Date',
                        default: frappe.datetime.get_today()
                    },
                    {
                        fieldname: 'amount',
                        fieldtype: 'Currency',
                        label: 'Amount',
                        default: frm.doc.total
                    }
                ], function(values) {
                    // Send payment data to API
                    var paymentData = {
                        attachment: values.attachment,
                        amount: values.amount,
                        name: frm.doc.name,
                        payment_date: values.transfer_date
                    };

                    frappe.call({
                        'method': 'school.school.doctype.fees.fees.pay',
                        'args': {
                            'payment_data': paymentData
                        },
                        'callback': function(r) {
                            if (r.message) {
                                frm.reload_doc();
                            }
                        }
                    })
                    // Call your payment API here and handle the response
                    // ...
                }, 'Payment Details');
            });
        }

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
