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
        # Retrieves the ID of the 'sale.view_order_form' view from the database to call it in action later
        job_costing_form_view_id = self.env.ref('tk_construction_management.job_costing_form_view').id

        # Assuming you have 'material_ids' and 'default_qty' as follows:
        material_ids = [50, 40]  # Replace with the actual list of IDs

        # Get the list of sale order lines IDs
        product_ids = self.order_line.product_id.ids
        _logger.info(f'\n*****\n product_ids: {product_ids} \n*****')
        default_qty = 7


        product_qty_dict = {}

        # Loop through each 'sale.order.line' record using the ids
        # The result is product_qty_dict = {product_id: [product_uom_qty, price_unit]}
        for order_line_id in product_ids:
            order_line = self.env['sale.order.line'].browse(order_line_id)
            _logger.info(f'\n*****\n order_line: {order_line} \n*****')
            product_qty = order_line.product_uom_qty
            _logger.info(f'\n*****\n product_qty: {product_qty} \n*****')
            product_qty_dict[order_line_id] = product_qty
            
        _logger.info(f'\n*****\n product_qty_dict = {product_qty_dict} \n*****')

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
    

    def cretae_job_costing3(self):
        # Retrieves the ID of the 'sale.view_order_form' view from the database to call it in action later
        job_costing_form_view_id = self.env.ref('tk_construction_management.job_costing_form_view').id
        print('===============================')

        # Get the list of sale order lines IDs
        product_ids = self.order_line.product_id.ids
        _logger.info(f'\n*****\n product_ids: {product_ids} \n*****')

        order_line_ids = self.order_line.ids
        _logger.info(f'\n*****\n order_line_ids: {order_line_ids} \n*****')

        # Make a dict in format:
        # {product_id: {'qty': float, 'price_unit': float, 'is_material': bool, 
        #                  'is_equipment': bool, 'is_expense_product': bool,...}}
        
        material_lines = []
        equipment_lines = []
        for order_line_id in order_line_ids:
            product_qty_dict = {}
            order_line = self.env['sale.order.line'].browse(order_line_id)
            _logger.info(f'\n*****\n order_line: {order_line} \n*****')

            product_id = order_line.product_id.id
            _logger.info(f'\n*****\n product_id: {product_id} \n*****')

            product_qty = order_line.product_uom_qty
            _logger.info(f'\n*****\n product_qty: {product_qty} \n*****')

            price_unit = order_line.price_unit
            price_reduce_taxinc = order_line.price_reduce_taxinc
            _logger.info(f'\n*****\n price_unit: {price_unit} \n*****')

            is_equipment = order_line.product_id.is_equipment
            is_material = order_line.product_id.is_material
            is_expense_product = order_line.product_id.is_expense_product
            detailed_type = order_line.product_id.detailed_type

            if is_material and detailed_type == 'product':
                product_qty_dict = {
                    'material_id': product_id, 'qty': product_qty, 
                    'cost': price_reduce_taxinc
                    }    
                material_lines.append(product_qty_dict)

            elif is_equipment and detailed_type == 'product':
                product_qty_dict = {
                    'equipment_id': product_id, 'qty': product_qty, 
                    'cost': price_reduce_taxinc, 
                    }    
                equipment_lines.append(product_qty_dict)
                

        _logger.info(f'\n*****\n  material_lines = {material_lines} \n*****')
        _logger.info(f'\n*****\n  equipment_lines = {equipment_lines} \n*****')


        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'job.costing', 
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': job_costing_form_view_id,
            'target': 'current',
            'context': {
                'default_material_ids': [(0, 0, line) for line in material_lines], # a list of tuples to fill One2many filed 'material_ids'
                'default_equipment_ids': [(0, 0, line) for line in equipment_lines], # a list of tuples to fill One2many filed 'equpment_ids'
 #               'default_eng_labour_ids': [(0, 0, {'role_id': 1, 'cost': 77})]
                 }
                }
        return action