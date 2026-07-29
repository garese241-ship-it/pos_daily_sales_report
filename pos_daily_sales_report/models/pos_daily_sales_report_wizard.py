# -*- coding: utf-8 -*-
from datetime import datetime, time, timedelta

import pytz

from odoo import api, fields, models
from odoo.exceptions import UserError


class PosDailySalesReportWizard(models.TransientModel):
    _name = 'pos.daily.sales.report.wizard'
    _description = "Assistant - État des ventes quotidiennes"

    def _default_date_from(self):
        today = fields.Date.context_today(self)
        return today.replace(day=1)

    date_from = fields.Date(string="Du", required=True, default=_default_date_from)
    date_to = fields.Date(string="Au", required=True, default=fields.Date.context_today)
    pos_config_ids = fields.Many2many(
        'pos.config',
        string="Points de vente",
        help="Laisser vide pour inclure tous les points de vente.",
    )
    company_id = fields.Many2one(
        'res.company',
        string="Société",
        required=True,
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one(related='company_id.currency_id', string="Devise")

    line_ids = fields.One2many('pos.daily.sales.report.line', 'wizard_id', string="Détail par jour")

    total_pos_sales = fields.Monetary(string="Total ventes POS", currency_field='currency_id')
    total_normal_sales = fields.Monetary(string="Total ventes normales", currency_field='currency_id')
    total_global = fields.Monetary(string="Total global de la période", currency_field='currency_id')

    has_results = fields.Boolean(string="Résultats générés", default=False)

    # ------------------------------------------------------------------
    # Calculs
    # ------------------------------------------------------------------
    def _get_day_bounds_utc(self, day):
        """Bornes UTC (naive) correspondant à une journée calendaire complète
        dans le fuseau horaire de la société."""
        tz_name = self.company_id.partner_id.tz or 'UTC'
        tz = pytz.timezone(tz_name)
        local_start = tz.localize(datetime.combine(day, time.min))
        local_end = tz.localize(datetime.combine(day, time.max))
        return (
            local_start.astimezone(pytz.UTC).replace(tzinfo=None),
            local_end.astimezone(pytz.UTC).replace(tzinfo=None),
        )

    def _get_pos_sales_for_day(self, start_utc, end_utc):
        self.ensure_one()
        domain = [
            ('date_order', '>=', start_utc),
            ('date_order', '<=', end_utc),
            ('state', 'in', ('paid', 'done', 'invoiced')),
            ('company_id', '=', self.company_id.id),
        ]
        if self.pos_config_ids:
            domain.append(('config_id', 'in', self.pos_config_ids.ids))
        orders = self.env['pos.order'].search(domain)
        return sum(orders.mapped('amount_total'))

    def _get_normal_sales_for_day(self, day):
        self.ensure_one()
        domain = [
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('invoice_date', '=', day),
            ('company_id', '=', self.company_id.id),
        ]
        invoices = self.env['account.move'].search(domain)
        if not invoices:
            return 0.0
        # Exclure les factures déjà générées depuis une commande POS
        pos_linked_invoice_ids = self.env['pos.order'].search([
            ('account_move', 'in', invoices.ids),
        ]).mapped('account_move').ids
        invoices = invoices.filtered(lambda inv: inv.id not in pos_linked_invoice_ids)
        return sum(invoices.mapped('amount_total'))

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def action_generate(self):
        self.ensure_one()
        if self.date_from > self.date_to:
            raise UserError("La date de début doit être antérieure ou égale à la date de fin.")

        max_days = 366
        if (self.date_to - self.date_from).days + 1 > max_days:
            raise UserError(
                "La période sélectionnée est trop longue (limite : "
                + str(max_days) + " jours). Réduis la période pour générer l'état."
            )

        self.line_ids.unlink()

        lines_vals = []
        current = self.date_from
        while current <= self.date_to:
            start_utc, end_utc = self._get_day_bounds_utc(current)
            pos_sales = self._get_pos_sales_for_day(start_utc, end_utc)
            normal_sales = self._get_normal_sales_for_day(current)
            lines_vals.append((0, 0, {
                'date': current,
                'pos_sales': pos_sales,
                'normal_sales': normal_sales,
            }))
            current += timedelta(days=1)

        self.line_ids = lines_vals
        self.total_pos_sales = sum(self.line_ids.mapped('pos_sales'))
        self.total_normal_sales = sum(self.line_ids.mapped('normal_sales'))
        self.total_global = self.total_pos_sales + self.total_normal_sales
        self.has_results = True

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'pos.daily.sales.report.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_print_pdf(self):
        self.ensure_one()
        if not self.has_results:
            self.action_generate()
        return self.env.ref(
            'pos_daily_sales_report.action_report_pos_daily_sales'
        ).report_action(self)
