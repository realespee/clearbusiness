# Copyright (c) 2024, Simon Wanyama and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ClearBusiness(Document):
	pass


@frappe.whitelist()
def deactivate_personnel(personnel):
	if personnel and frappe.db.exists('ClearPersonnel', personnel):
		doc = frappe.get_doc('ClearPersonnel', personnel)
		if doc.active:
			doc.active = 0
			doc.save()
		frappe.db.commit()
	return f'Personnel {personnel} deactivated!'