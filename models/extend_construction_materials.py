from odoo import models, fields, api
from odoo.exceptions import RedirectWarning
import logging


_logger = logging.getLogger(__name__)


class ConstructionMaterial(models.Model):
    _inherit = 'construction.material'

    # name = fields.Char(string="Title")
    # date = fields.Date(string="Date", default=fields.Date.today())
    # construction_id = fields.Many2one('construction.details', string="Construction")
    # construction_material_ids = fields.One2many('construction.material.line', 'construction_material_id',
    #                                             string="Material")
    # company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    # currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency')
    # material_po_id = fields.Many2one('purchase.order', string="Purchase Order")
    # total_material_cost = fields.Monetary(string="Total Cost", compute="_compute_material_cost")
    # state = fields.Selection(related="material_po_id.state", string="State")
    # job_type_id = fields.Many2one('construction.job', string="Job Type")

    def create(self, vals):
        print(f'********construction.material - create = {vals}')