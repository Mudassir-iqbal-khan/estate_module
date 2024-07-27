from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        comodel_name='estate.property',
        inverse_name='user_id',  # Adjust this to match your field for the salesperson
        string='Properties',
        domain=[('status', '=', 'available')]  # Adjust this domain to match your criteria
    )
