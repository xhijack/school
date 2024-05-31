// Copyright (c) 2024, PT Sopwer Teknologi Indonesia and contributors
// For license information, please see license.txt

frappe.ui.form.on("Fees Schedule", {
    refresh(frm){
            frm.add_custom_button(__('Get All Students'), function() {
                student_class = [];
                frm.doc.student_class.forEach(element => {
                    student_class.push(element.class_student); 
                });
                console.log(student_class)
                frappe.call({
                    method: 'school.school.doctype.fees_schedule.fees_schedule.get_all_students',
                    args: {
                        academic_year: frm.doc.academic_year,
                        student_class: student_class
                    },
                    callback: function(r) {
                        if (r.message) {
                            frm.set_value('students', r.message);
                            frm.refresh_field('students');
                            console.log(r.message)
                        }
                    }
                });
            });
            if (frm.doc.docstatus == 1){
                frm.add_custom_button(__('Create Fees'), function() {
                    frappe.call({
                        method: 'school.school.doctype.fees_schedule.fees_schedule.create_fees',
                        args: {
                            fees_schedule: frm.doc.name
                        },
                        freeze: true,
                        freeze_message: 'Sedang membuat tagihan...',
                        callback: function(r) {
                            if (r.message) {
                                frappe.msgprint('Membuat pembayaran berhasil');
                            }
                        }
                    });
                });
    
            }
        
    }
})

frappe.ui.form.on("Fees Schedule Class", {
	class: function(frm, cdt, cdn) {
           
	}
});

function calculate_total_students(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    frappe.model.set_value(row.doctype, row.name, 'total_students', row.rate * row.qty);
    calculate_total(frm);
}

