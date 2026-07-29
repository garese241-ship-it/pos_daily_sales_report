# POS Daily Sales Report

Module Odoo qui affiche un état du chiffre d'affaires quotidien sur une
période choisie : ventes POS, ventes normales (factures), et total de la
période.

## Fonctionnalités

- Choix libre de la période (dates de début et de fin).
- Filtrage optionnel par un ou plusieurs points de vente.
- Une ligne par jour de la période, même les jours sans activité (à 0).
- Détail des ventes POS et des ventes normales (factures clients hors POS)
  pour chaque jour, sans doublon entre les deux.
- Total de la période affiché automatiquement en bas du tableau.
- Consultation à l'écran et export PDF.
- Intégré directement dans les menus **Point de Vente** et **Ventes**.

## Compatibilité

| Série Odoo | Branche | Statut |
|---|---|---|
| 17.0 | `17.0` | Testé en production |
| 18.0 | `18.0` | Beta — à valider avant mise en production |
| 19.0 | `19.0` | Beta — à valider avant mise en production |

## Installation

1. Copier le dossier du module dans votre répertoire d'addons custom.
2. Redémarrer le service Odoo.
3. Activer le mode développeur, aller dans **Apps**, retirer le filtre
   "Apps", rechercher `pos_daily_sales_report`, installer.
4. Le menu **État des ventes quotidiennes** apparaît sous **Point de Vente**
   et sous **Ventes**.

## Licence

LGPL-3. Voir https://www.gnu.org/licenses/lgpl-3.0.html

## Auteur

GARESE — https://www.garese.net

## Support

Ce module est fourni gratuitement, sans garantie de support. Les
suggestions et rapports de bug sont les bienvenus via les issues GitHub.
