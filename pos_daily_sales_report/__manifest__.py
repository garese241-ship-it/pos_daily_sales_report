# -*- coding: utf-8 -*-
{
    'name': "POS Daily Sales Report",
    'version': '17.0.1.0.0',
    'category': 'Point of Sale',
    'summary': "État du chiffre d'affaires quotidien (POS + ventes normales) sur une période, à l'écran et en PDF",
    'description': """
POS Daily Sales Report
=======================

Affiche un état jour par jour du chiffre d'affaires sur une période choisie :

- Une ligne par jour de la période (même les jours sans activité, à 0).
- Le détail des ventes POS et des ventes normales (factures hors POS) pour
  chaque jour.
- Le total de la période en bas du tableau.
- Filtrage optionnel par point(s) de vente.
- Consultation à l'écran et export PDF.

Configuration
-------------
Accessible depuis le menu **État des ventes quotidiennes** (visible par les
managers POS). Aucune configuration technique n'est nécessaire.
""",
    'author': 'GARESE',
    'website': 'https://www.garese.net',
    'license': 'LGPL-3',
    'images': [
        'static/description/icon.png',
    ],
    'depends': ['point_of_sale', 'account', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/pos_daily_sales_report_views.xml',
        'report/pos_daily_sales_report_templates.xml',
        'report/pos_daily_sales_report_actions.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
