# Copyright (c) 2024, Simon Wanyama and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ClearPersonnel(Document):
	def before_save(self):
		self.full_name = f'{self.first_name} {self.last_name}'

	def after_insert(self):
		self.update_business_staff()

	def on_update(self):
		self.update_business_staff()

	def update_business_staff(self):
		if self.personnel_type == "Business Staff" and self.business:
			business_doc = frappe.get_doc('ClearBusiness', self.business)

		existing_staff = next((staff for staff in business_doc.get('business_staff') if staff.staff_name == self.name), None)

		staff_data = {
			"staff_name": self.name,
			"resident_status": self.resident_status,
			"email_address": self.email_address,
			"phone_number": self.phone_number
		}

		if existing_staff:
			for field, value in staff_data.items():
				setattr(existing_staff, field, value)
		else:
			business_doc.append('business_staff', staff_data)

		business_doc.save()