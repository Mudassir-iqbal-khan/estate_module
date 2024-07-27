from datetime import datetime, timedelta
from odoo.tools import float_compare, float_is_zero

from odoo.exceptions import UserError, ValidationError

from odoo import fields, models, api


class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "Real-Estate Properties"

    name = fields.Char(string="Name", required=True)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price")
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.'),
        ('unique_name', 'UNIQUE(name)', 'The property name must be unique.')
    ]

    title = fields.Char(string='Title')
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string='Availability From', copy=False,
                                    default=lambda self: (datetime.today() + timedelta(days=90)).date())
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Float(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Float(string="Garden Area (sqm)")
    user_id = fields.Many2one('res.users', string='Salesperson')

    garden_orientation = fields.Selection(
        [('north', 'North'),
         ('south', 'South'),
         ('east', 'East'),
         ('west', 'West')],
        string="Garden Orientation"
    )

    property_type_id = fields.Many2one('estate.property.type', string='Property Types')

    total_area = fields.Float(string="Total Area (sqm)", compute='_compute_total_area', store=True)
    best_price = fields.Float(string="Best_offer", compute='_compute_best_price', store=True)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                delta = offer.date_deadline - offer.create_date.date()
                offer.validity = delta.days
            elif not offer.create_date and offer.date_deadline:
                delta = offer.date_deadline - fields.Date.today()
                offer.validity = delta.days

    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('sold', 'Sold'),
    ], string='State', default='new')

    status = fields.Selection([
        ('new', 'New'),
        ('sold', 'Sold'),
        ('cancel', 'Cancelled')
    ], default='new', string='Status')

    buyer_id = fields.Many2one('res.partner', string='Buyer')
    salesperson_id = fields.Many2one('res.users', string='Salesperson')
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

    @api.model
    def _get_default_date_availability(self):
        return (datetime.today() + timedelta(days=90)).date()
    date_availability = fields.Date(string="Availability Date", copy=False, default=_get_default_date_availability)

    def edit_button_action(self):
        self.ensure_one()
        # Logic to handle the edit button action
        return {
            'type': 'ir.actions.act_window',
            'name': 'Edit Property',
            'res_model': 'estate.property',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'target': 'current',
        }

    def create_button_action(self):
        # Logic to handle the create button action
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Property',
            'res_model': 'estate.property',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        }

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 50.0  # Example default value
            self.garden_orientation = 'north'  # Example default value
        else:
            self.garden_area = 0.0
            self.garden_orientation = False

    def action_sold(self):
        for property in self:
            if property.status == 'cancel':
                raise UserError("Cancelled property cannot be set as sold.")
            property.status = 'new'

    def action_cancel(self):
        for property in self:
            property.status = 'cancel'

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_rounding=0.01):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_rounding=0.01) < 0:
                    raise ValidationError(
                        "The selling price cannot be lower than 90% of the expected price."
                    )