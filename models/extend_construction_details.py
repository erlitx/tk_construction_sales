from odoo import models, fields, api
from odoo.exceptions import RedirectWarning
import logging


_logger = logging.getLogger(__name__)


class ConstructionMaterial(models.Model):
    _inherit = 'construction.details'



    my_field = fields.Char(string="TEST")


    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        res['my_field'] = 'HELLO'
        res['estimate_cost'] = 123
        print(f'----------res ----> {res}')
        res['equipment_ids'] = [(0, 0, {'name': 'New equipment', 'job_type_id': 1})]

        context = dict(self._context or {})
        context['default_job_costing_id'] = 2
        self = self.with_context(context)
        print(f'----------context ----> {context}')
        return res



class ConstructionEquipment(models.Model):
    _inherit = 'construction.equipment'

    # Method called whenever a new form view is opened for this model
    # Add some default values
    @api.model
    def default_get(self, fields):
        context = dict(self._context or {})
        print(f'----------context eq----> {context}')
        res = super().default_get(fields)
        print(f'----------res construction.equipment ----> {res}')
        #self.job_costing_id
        print(f'----------job_costing_id ----> {self.construction_id}')
        # job_costing_ids = self.env['job.costing'].browse(self.job_costing_id)
        # print(f'----------job_costing_ids ----> {job_costing_ids}')

        res['name'] = 'New title'
        res['construction_equipment_ids'] = [(0, 0, {'equipment_id': 84})]
        # equipment_ids = [{'equipment_ids': id for id in self.env['job.costing'].browse(self.job_order_id)}]
        # res['construction_equipment_ids'] = [(0, 0, id) for id in equipment_ids] 
        # equipment_ids
        #print(f'----------res eqipment ----> {res}')
        return res
    
    def custom_button(self):
        pass


    # @api.model
    # def read(self, fields=None, load='_classic_read'):
    #     # Call the super method to perform the default behavior of the read() method.
    #     records = super().read(fields=fields, load=load)
    #     print(f'-----read---->')
    #     # default_estimate_cost = 123  # Set your desired default value here  
    #     # for record in records:
    #     #     # Set the default value for the estimate_cost field
    #     #     record['estimate_cost'] = default_estimate_cost
    #     return records



class ConstructionEquipmentLine(models.Model):
    _inherit = 'construction.equipment.line'

    # @api.model
    # def default_get(self, fields):
    #     res = super().default_get(fields)
    #     print(f'--------construction.equipment.line ----> {res}')
    #     return res

