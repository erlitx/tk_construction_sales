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

    def action_create_job_order(self):
        context = self.env.context
        print(f'-----context = {context}')
        # Get the current context as a mutable dictionary
        context = dict(self.env.context)

        if 'default_material_ids' in context:
            context.pop('default_material_ids')
        if 'default_equipment_ids' in context:
            context.pop('default_equipment_ids')

        self = self.with_context(context)
        print(f'-----context = {context}')
        # Call the original method 
        result = super(CustomJobCosting, self).action_create_job_order()
        return result
    
