# Copyright (c) 2024, PT Sopwer Teknologi Indonesia and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Fees(Document):
	def validate(self):

		self.validator = PriodUniqValidator()
	

		self.calculate_total()

	def calculate_total(self):
		total = 0
		for fee in self.fees_detail:
			total += fee.amount
		self.total = total
	
	def on_submit(self):
		if self.docstatus == 1:
			self.status = 'Unpaid'
			frappe.db.set_value('Fees', self.name, 'status', 'Unpaid')
			for fee in self.fees_detail:
				
				self.validator.validate({'priod': self.priod, 'student': self.student, 'fee_category': fee.fees_category, 'docstatus': 1})

				fees_ledger = frappe.new_doc("Fees Ledger")
				fees_ledger.student = self.student
				fees_ledger.date = self.date
				fees_ledger.priod = self.priod
				fees_ledger.fee_category = fee.fees_category
				fees_ledger.amount = fee.amount
				fees_ledger.status = self.status
				fees_ledger.party_type = 'Fees'
				fees_ledger.party = self.name
				fees_ledger.submit()
	
	def on_cancel(self):
		if self.docstatus == 2:
			frappe.db.set_value('Fees', self.name, 'status', 'Cancelled')
			frappe.db.set_value('Fees Ledger', {'party': self.name}, 'status', 'Cancelled')


class Validator:
    def __init__(self, successor=None):
        self._successor = successor

    def set_successor(self, successor):
        self._successor = successor

    def validate(self, data):
        if self._successor:
            return self._successor.validate(data)
        return True

class PriodUniqValidator(Validator):
	def validate(self, data):
		if frappe.db.exists('Fees Ledger', {'priod': data.get('priod'), 'student': data.get('student'), 'fee_category': data.get('fee_category'), 'docstatus': 1 }):
			frappe.throw('Priod already exists')
		return super().validate(data)


@frappe.whitelist()
def get_fee_structure_details(fee_structure):
	fee_structure_details = frappe.get_all('Fee Structure Detail', filters={'parent': fee_structure}, fields=['*'])
	return fee_structure_details
	
@frappe.whitelist()
def pay(payment_data):
	payment_data = frappe.parse_json(payment_data)
	# import pdb
	# pdb.set_trace()
	frappe.db.set_value('Fees', payment_data['name'], 'status', 'Paid')
	frappe.db.set_value('Fees', payment_data['name'], 'payment_date', payment_data['payment_date'])


	if payment_data.get('attachment'):
		files = frappe.get_all('File', filters={'file_name': payment_data['attachment']}, fields=['*'])

		if files:
			frappe.db.set_value('File',files[0].name,'attached_to_doctype', 'Fees')
			frappe.db.set_value('File',files[0].name,'attached_to_name', payment_data['name'])


	frappe.db.set_value('Fees Ledger', {'party': payment_data['name']}, 'status', 'Paid')
	frappe.db.set_value('Fees Ledger', {'party': payment_data['name']}, 'payment_date',  payment_data['payment_date'])
	frappe.db.commit()
	return "success"