# Copyright (c) 2024, PT Sopwer Teknologi Indonesia and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Fees(Document):
	def validate(self):
		pass


@frappe.whitelist()
def get_fee_structure_details(fee_structure):
	fee_structure_details = frappe.get_all('Fee Structure Detail', filters={'parent': fee_structure}, fields=['*'])
	return fee_structure_details
	