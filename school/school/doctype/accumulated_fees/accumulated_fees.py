# Copyright (c) 2024, PT Sopwer Teknologi Indonesia and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AccumulatedFees(Document):
	def validate(self):
		self.total = sum([item.amount for item in self.priod_list])

	def on_submit(self):
		if self.docstatus == 1:
			# self.status = 'Unpaid'
			# frappe.db.set_value('Fees', self.name, 'status', 'Unpaid')
			frappe.db.set_value('Accumulated Fees', self.name, 'status', 'Unpaid')
			for priod in self.priod_list:
				fee = frappe.new_doc('Fees')
				fee.student = self.student
				fee.date = self.posting_date
				fee.academic_year = self.academic_year
				fee.priod = priod.priod
				fee.payment_due_date = self.posting_date
				fee.fee_structure = self.fee_structure
				fee.total_fees = priod.amount

				for fee_structure in frappe.get_all('Fee Structure', {'name': self.fee_structure}):
					fee_structure_ = frappe.get_doc('Fee Structure', fee_structure.name)
					for fee_structure_detail in fee_structure_.fee_structure_detail:
						fee_detail = fee.append('fees_detail', {})
						fee_detail.fees_category = fee_structure_detail.fees_category
						fee_detail.amount = fee_structure_detail.amount

				fee.submit()
				frappe.db.set_value('Fees', fee.name, 'party_type', 'Accumulated Fees')
				frappe.db.set_value('Fees', fee.name, 'party', self.name)
			frappe.db.commit()

