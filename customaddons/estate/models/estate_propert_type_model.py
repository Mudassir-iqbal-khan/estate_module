from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'

    name = fields.Char(string='Name', required=True)
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'The property type name must be unique.')
    ]

    def action_save(self):
        # Logic to handle the save action
        # You can add custom logic here if needed
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_discard(self):
        # Logic to handle the discard action
        # You can add custom logic here if needed
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

