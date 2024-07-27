from datetime import timedelta

from odoo import fields, models, api, exceptions


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(string='Price', required=True)
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.')
    ]

    status = fields.Selection([
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string='Status', default='new')

    def action_accept(self):
        for offer in self:
            if offer.status not in ['accepted', 'refused']:
                existing_accepted_offer = self.search([
                    ('property_id', '=', offer.property_id.id),
                    ('status', '=', 'accepted')
                ])
                if existing_accepted_offer:
                    raise exceptions.UserError("Another offer is already accepted for this property.")
                offer.status = 'accepted'
                offer.property_id.buyer_id = offer.partner_id
                offer.property_id.selling_price = offer.price

    def action_refuse(self):
        for offer in self:
            if offer.status not in ['accepted', 'refused']:
                offer.status = 'refused'

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                delta = offer.date_deadline - offer.create_date.date()
                offer.validity = delta.days
            elif not offer.create_date and offer.date_deadline:
                delta = offer.date_deadline - fields.Date.today()
                offer.validity = delta.days


