from odoo import models, fields, api


class CustomJobCosting(models.Model):
    _inherit = "job.costing"

    new_field = fields.Char(string="New Field")
    