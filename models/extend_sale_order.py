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
       # _logger.info(f'\n*****\n self.order_line.product_uom_qty: {self.order_line.product_uom_qty} \n*****')
        _logger.info(f'\n*****\n self.order_line: {self.order_line} \n*****')

        for order_line in self.order_line:
            print(f'----------order_line: {order_line}')


###############
        # order_line_id = self.order_line.id
        # _logger.info(f'\n*****\n order_lines: {order_line_id} \n*****')
        # lines = self.env['sale.order.line'].search([('id', '=', order_line_id)])
        # _logger.info(f'\n*****\n lines: {lines.product_uom_qty} \n*****')
###############


        order_line_products = product_id.ids        # the list of product from Sale order
        cost_material_lines = []

        # Get the list of Products ID from 'cost.material.line' (not the IDs of product.product)
        for product_id in order_line_products:
            # Get an ID of product in 'cost.material.line'
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
            'context': {'default_material_ids': cost_material_lines,
                        } # pass the ID list of products ('cost.material.line')

        }
        return action
    






    def cretae_job_costing2(self):
        # Retrieves the ID of the 'sale.view_order_form' view from the database
        job_costing_form_view_id = self.env.ref('tk_construction_management.job_costing_form_view').id

        # Assuming you have 'material_ids' and 'default_qty' as follows:
        material_ids = [50, 40]  # Replace with the actual list of IDs
        product_ids = self.order_line.product_id.ids
        default_qty = 7

        # Create a list of dictionaries with 'material_id' and 'qty'
        material_lines = [{'material_id': material_id, 'qty': default_qty} for material_id in product_ids]

        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'job.costing', 
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': job_costing_form_view_id,
            'target': 'current',
            'context': {
                'default_material_ids': [(0, 0, line) for line in material_lines], # a list of tuples to fill One2many filed 'material_ids'
                'default_equipment_ids': [(0, 0, {'equipment_id': 50, 'qty': 77})], # a list of tuples to fill One2many filed 'equpment_ids'
                'default_eng_labour_ids': [(0, 0, {'role_id': 1, 'cost': 77})]
    }
}



#         material_id = 1
#         default_qty = 5


#         # Prepare the action dictionary for redirection
#         action = {
#             'type': 'ir.actions.act_window',
#             'res_model': 'job.costing', 
#             'view_mode': 'form',
#             'view_type': 'form',
#             'view_id': job_costing_form_view_id,
#             'target': 'current',
#             'context': {'default_material_ids': [(0, 0, {'material_id': material_id, 'qty': default_qty})]
# }
#         }
        return action