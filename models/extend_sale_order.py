from odoo import models, fields, api
from odoo.exceptions import RedirectWarning
import logging


_logger = logging.getLogger(__name__)


class CustomSaleOrder(models.Model):
    _inherit = "sale.order"


    def cretae_job_costing(self):
        # Get the list of sale order lines IDs
        order_line_ids = self.order_line.ids

        material_lines = [] # a list to pass with a context to 'material_ids' O2M fieled of 'job.costing' model
        equipment_lines = [] # a list to pass with a context to 'equipment_ids' O2M fieled of 'job.costing' model

        # Loop over all 'sale.order.lines'
        for order_line_id in order_line_ids:
            # A temporary dict with the values of each sale order line 
            product_qty_dict = {}
            order_line = self.env['sale.order.line'].browse(order_line_id)

            product_id = order_line.product_id.id                   # get a product ID
            product_qty = order_line.product_uom_qty                # get a product qty from a line
            price_unit = order_line.price_unit                      # get a non-taxed product unit price
            price_reduce_taxinc = order_line.price_reduce_taxinc    # get a tax-incl product unit price
            is_equipment = order_line.product_id.is_equipment       # get a product bool value of 'is_equipment'
            is_material = order_line.product_id.is_material         # get a product bool value of 'is_material'
            is_expense_product = order_line.product_id.is_expense_product
            detailed_type = order_line.product_id.detailed_type     # get a product value of 'Product Type' field

            # If a product type is a 'product' and it's a 'material' put order.line values to a 
            # material_lines list 
            if is_material and detailed_type == 'product':
                product_qty_dict = {
                    'material_id': product_id, 'qty': product_qty, 
                    'cost': price_reduce_taxinc
                    }    
                material_lines.append(product_qty_dict)

            # If a product type is a 'product' and it's a 'equipment' put order.line values to a  
            # equipment_lines list
            elif is_equipment and detailed_type == 'product':
                product_qty_dict = {
                    'equipment_id': product_id, 'qty': product_qty, 
                    'cost': price_reduce_taxinc, 
                    }    
                equipment_lines.append(product_qty_dict)

        # Retrieves the ID of the 'sale.view_order_form' view from the database to call it in action
        job_costing_form_view_id = self.env.ref('tk_construction_management.job_costing_form_view').id

        # This dict returned in Odoo with a function will open a new form view 'job_costing_form_view_id'
        # and pass a context to fill in materials/equipment fields with values
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
                 # 'default_eng_labour_ids': [(0, 0, {'role_id': 1, 'cost': 77})]
                 }
                }
        return action