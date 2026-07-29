# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PosDailySalesReportLine(models.TransientModel):
    _name = 'pos.daily.sales.report.line'
    _description = "Ligne de l'état des ventes quotidiennes"
    _order = 'date asc'

    wizard_id = fields.Many2one(
        'pos.daily.sales.report.wizard',
        required=True,
        ondelete='cascade',
    )
    date = fields.Date(string="Date", required=True)
    day_label = fields.Char(string="Jour", compute='_compute_day_label', store=True)
    pos_sales = fields.Monetary(string="Ventes POS", currency_field='currency_id')
    normal_sales = fields.Monetary(string="Ventes normales", currency_field='currency_id')
    total = fields.Monetary(
        string="Total du jour",
        compute='_compute_total',
        store=True,
        currency_field='currency_id',
    )
    currency_id = fields.Many2one(related='wizard_id.currency_id')

    @api.depends('date')
    def _compute_day_label(self):
        for line in self:
            if not line.date:
                line.day_label = ''
                continue
            lang_code = line.wizard_id.env.user.lang or 'fr_FR'
            try:
                from babel.dates import format_date
                line.day_label = format_date(line.date, format='EEEE dd/MM/yyyy', locale=lang_code)
            except Exception:
                line.day_label = line.date.strftime('%A %d/%m/%Y')

    @api.depends('pos_sales', 'normal_sales')
    def _compute_total(self):
        for line in self:
            line.total = (line.pos_sales or 0.0) + (line.normal_sales or 0.0)
