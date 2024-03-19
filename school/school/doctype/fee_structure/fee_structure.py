# Copyright (c) 2024, PT Sopwer Teknologi Indonesia and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FeeStructure(Document):
	def validate(self):
		self.total = sum([d.amount for d in self.fee_structure_detail])
