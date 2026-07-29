# -*- coding: utf-8 -*-
{
    'name': "POS Daily Sales Report",
    'version': '18.0.1.0.0',
    'category': 'Point of Sale',
    'summary': "État du chiffre d'affaires quotidien (POS + ventes normales) sur une période, à l'écran et en PDF",
    'description': """
POS Daily Sales Report (v18 — build non testée en production)
=================================================================

Cette version cible Odoo 18.0. Le code est identique à la version 17.0
(la seule différence connue concerne la syntaxe des vues XML : balise
<list> au lieu de <tree>), mais elle n'a pas encore été validée sur une
instance Odoo 18 réelle. Testez en environnement de recette avant mise
en production.

Affiche un état jour par jour du chiffre d'affaires sur une période choisie :

- Une ligne par jour de la période (même les jours sans activité, à 0).
- Le détail des ventes POS et des ventes normales (factures hors POS) pour
  chaque jour.
- Le total de la période en bas du tableau.
- Filtrage optionnel par point(s) de vente.
- Consultation à l'écran et export PDF.
- Intégré dans les menus Point de Vente et Ventes.

Configuration
-------------
Accessible depuis le menu **État des ventes quotidiennes**, sous
**Point de Vente** ou **Ventes** (visible par les managers POS). Aucune
configuration technique n'est nécessaire.
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
