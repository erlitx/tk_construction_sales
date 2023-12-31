from odoo import models, fields, api


class CustomJobCosting(models.Model):
    _inherit = "job.costing"

    sale_order_id = fields.Many2one('sale.order', string='Sale Order')


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
    
    # Get 'name' field value from context
    @api.model
    def create(self, vals):
        if vals.get('name', ('New')) == ('New'):
            context = self._context or {}
            default_name = context.get('default_name')
            vals['name'] = default_name or self.env['ir.sequence'].next_by_code('job.costing') or ('New')
        
        # Clear context
        context = self.env.context
        print(f'-----context = {context}')
        # Get the current context as a mutable dictionary
        context = dict(self.env.context)

        if 'default_material_ids' in context:
            context.pop('default_material_ids')
        if 'default_equipment_ids' in context:
            context.pop('default_equipment_ids')
        if 'default_name' in context:
            context.pop('default_name')
        if 'default_site_id' in context:
            context.pop('default_site_id')

        self = self.with_context(context)
        print(f'-----context = {context}')
        res = super(CustomJobCosting, self).create(vals)

        return res