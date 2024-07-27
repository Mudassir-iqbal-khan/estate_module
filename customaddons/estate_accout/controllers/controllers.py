# -*- coding: utf-8 -*-
# from odoo import http


# class EstateAccout(http.Controller):
#     @http.route('/estate_accout/estate_accout', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/estate_accout/estate_accout/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('estate_accout.listing', {
#             'root': '/estate_accout/estate_accout',
#             'objects': http.request.env['estate_accout.estate_accout'].search([]),
#         })

#     @http.route('/estate_accout/estate_accout/objects/<model("estate_accout.estate_accout"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('estate_accout.object', {
#             'object': obj
#         })
