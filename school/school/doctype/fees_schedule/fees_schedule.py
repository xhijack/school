# Copyright (c) 2024, PT Sopwer Teknologi Indonesia and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document


class FeesSchedule(Document):
	def validate(self):
		self.total = sum([s.total_fees for s in self.students])



@frappe.whitelist()
def get_all_students(academic_year, student_class):
	student_class = json.loads(student_class)
	# import pdb
	# pdb.set_trace()
 
	students_with_fees = []
	for sc in student_class:
		student_class_ = frappe.get_all('Student Class', {'academic_year': academic_year, 'student_class': sc})
		if student_class_:
			sc_ = frappe.get_doc('Student Class', student_class_[0].name)
			students = sc_.students
			for student in students:
				fs = frappe.get_all('Fee Structure', {'student': student.student, 'academic_year': academic_year})
				if fs:
					fee_structure = frappe.get_doc('Fee Structure', fs[0].name)
					students_with_fees.append({
						'student': student.student,
						'full_name': student.full_name,
						'student_class': sc,
						'fee_structure': fee_structure.name,
						'total_fees': fee_structure.total
					})
	
	return students_with_fees				

@frappe.whitelist()
def create_fees(fees_schedule):
	fs = frappe.get_doc('Fees Schedule', fees_schedule)
	for student in fs.students:
		fee = frappe.new_doc('Fees')
		fee.student = student.student
		fee.date = fs.posting_date
		fee.academic_year = fs.academic_year
		fee.priod = fs.priod
		fee.payment_due_date = fs.due_date
		fee.student_class = student.student_class
		fee.student_name = student.full_name
		fee.fee_structure = student.fee_structure
		fee.total_fees = student.total_fees

		for fee_structure in frappe.get_all('Fee Structure', {'name': student.fee_structure}):
			fee_structure_ = frappe.get_doc('Fee Structure', fee_structure.name)
			for fee_structure_detail in fee_structure_.fee_structure_detail:
				fee_detail = fee.append('fees_detail', {})
				fee_detail.fees_category = fee_structure_detail.fees_category
				fee_detail.amount = fee_structure_detail.amount

		fee.submit()
		frappe.db.set_value('Fees', fee.name, 'party_type', 'Fees Schedule')
		frappe.db.set_value('Fees', fee.name, 'party', fees_schedule)
	frappe.db.commit()
	return "success"
		