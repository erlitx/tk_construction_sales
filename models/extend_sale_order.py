from odoo import models, fields, api
from odoo.exceptions import RedirectWarning
import logging


_logger = logging.getLogger(__name__)


class CustomSaleOrder(models.Model):
    _inherit = "sale.order"

  #  new_field = fields.Char(string="New Field")


    def cretae_job_costing(self):
        # Retrieves the ID of the 'sale.view_order_form' view from the database
        job_costing_form_view_id = self.env.ref('tk_construction_management.job_costing_form_view').id

        # Get the product.product IDs from Sale Order
        product_id = self.order_line.product_id
        _logger.info(f'\n*****\n product_id: {product_id} \n*****')
        _logger.info(f'\n*****\n product_id.id: {product_id.ids} \n*****')

        order_line_products = product_id.ids        # the list of product from Sale order
        cost_material_lines = []

        # Get the list of Products ID from 'cost.material.line' (not the IDs of product.product)
        for product_id in order_line_products:
            product_line = self.env['cost.material.line'].search([('material_id', '=', product_id)], limit=1)
            product_line_id = product_line.id
            cost_material_lines.append(product_line_id)
        #cost_material_lines = self.env['cost.material.line'].search([('material_id', 'in', order_line_products)]).ids

        _logger.info(f'\n*****\n cost_material_line: {cost_material_lines} \n*****')

        # Prepare the action dictionary for redirection
        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'job.costing', 
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': job_costing_form_view_id,
            'target': 'current',
            'context': {'default_material_ids': cost_material_lines} # pass the ID list of products ('cost.material.line')

        }

        #print(f'---{action}')
        return action