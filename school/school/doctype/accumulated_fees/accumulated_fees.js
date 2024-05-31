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

        // Add Pay button
        if (frm.doc.status === "Unpaid") {
            frm.add_custom_button(__('Pay'), function() {
                // Open dialog for payment details
                frappe.prompt([

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
                        'method': 'school.school.doctype.accumulated_fees.accumulated_fees.pay',
                        'args': {
                            'accumulated_fees': frm.doc.name,
                            'payment_data': paymentData
                        },
                        'freeze': true,
                        'freeze_message': 'Processing Payment...',
                        'callback': function(r) {
                            if (r.message == 'success') {
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