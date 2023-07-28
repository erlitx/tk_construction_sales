from odoo import models, fields, api


class CustomJobCosting(models.Model):
    _inherit = "job.costing"

    # new_field = fields.Char(string="New Field")


    # Override the default create method
    # @api.model
    # def create(self, vals):
    #     # Print custom message before calling the default create method
    #     print("Custom create method is called with values:", vals)
    #     return super(CustomJobCosting, self).create(vals)