# -*- coding: utf-8 -*-
from pydantic_core.core_schema import lax_or_strict_schema

from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError


class WizardMergePurchaseOrder(models.TransientModel):
    _name = 'wizard.merge.purchase.order'

    type = fields.Selection([
        ('cancel', 'Create new Order and Cancel all selected Order'),
        ('delete', 'Create new Order and Delete all selected Order'),
        ('merge_cancel', 'Merge order into selected Order and cancel'),
        ('merge_delete', 'Merge order into selected Order and delete')
    ])
    purchase_order_ids = fields.Many2many('purchase.order')
    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order')

    @api.model
    def default_get(self, fields_list):
        res = super(WizardMergePurchaseOrder, self).default_get(fields_list)
        if self.env.context.get('active_model') == 'purchase.order':
            purchase_order = self.env['purchase.order'].search([
                ('id', 'in', self.env.context.get('active_ids'))
            ])
            res['purchase_order_ids'] = [(6, 0, purchase_order.ids)]
        return res

    def action_confirm(self):
        if not self.type:
            return True
        if any(self.purchase_order_ids.filtered(lambda x: x.state != 'draft')):
            raise UserError(_("You can only merge Purchase Order in Draft State"))
        if len(self.purchase_order_ids.mapped('partner_id')) > 1:
            raise UserError(_("Please select Purchase Order whose Vendors are same to perform the Merge Option"))
        if self.type in ['cancel', 'delete']:
            purchase_order = self.env['purchase.order'].create({
                'partner_id': self.purchase_order_ids[0].partner_id.id,
                'origin': "From " + ", ".join(pur.name for pur in self.purchase_order_ids) + ' Cancelled' if self.type == 'cancel' else "From " + ", ".join(pur.name for pur in self.purchase_order_ids) + ' Deleted'
            })
            for line in self.purchase_order_ids.mapped('order_line'):
                if line.product_id.id in purchase_order.order_line.mapped('product_id').ids:
                    line_product = purchase_order.order_line.filtered(lambda x: x.product_id.id == line.product_id.id)
                    line_product.product_qty += line.product_qty
                else:
                    self.env['purchase.order.line'].create({
                        'product_id': line.product_id.id,
                        'name': line.product_id.display_name,
                        'product_qty': line.product_qty,
                        'price_unit': line.price_unit,
                        'order_id': purchase_order.id
                    })
            for purchase in self.purchase_order_ids:
                if self.type == 'cancel':
                    purchase.button_cancel()
                else:
                    purchase.order_line.unlink()
                    purchase.button_cancel()
                    purchase.unlink()
        if self.type in ['merge_cancel', 'merge_delete']:
            self.purchase_order_id.origin = "From " + ", ".join(pur.name for pur in self.purchase_order_ids.filtered(lambda x: x.id != self.purchase_order_id.id)) + ' Cancelled' \
                if self.type == 'merge_cancel' else ", ".join(pur.name for pur in self.purchase_order_ids.filtered(lambda x: x.id != self.purchase_order_id.id)) + ' Deleted'
            for line in self.purchase_order_ids.filtered(lambda x: x.id != self.purchase_order_id.id).mapped('order_line'):
                if line.product_id.id in self.purchase_order_id.order_line.mapped('product_id').ids:
                    line_product = self.purchase_order_id.order_line.filtered(lambda x: x.product_id.id == line.product_id.id)
                    line_product.product_qty += line.product_qty
                else:
                    self.env['purchase.order.line'].create({
                        'product_id': line.product_id.id,
                        'name': line.product_id.display_name,
                        'product_qty': line.product_qty,
                        'price_unit': line.price_unit,
                        'order_id': self.purchase_order_id.id
                    })
            for purchase in self.purchase_order_ids.filtered(lambda x: x.id != self.purchase_order_id.id):
                if self.type == 'merge_cancel':
                    purchase.button_cancel()
                else:
                    purchase.order_line.unlink()
                    purchase.button_cancel()
                    purchase.unlink()


