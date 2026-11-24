# Order Prep & Staffing Analytics

Prototype d'analyse de charge et d'aide au dimensionnement d'équipe en préparation de commandes (contexte e-commerce / logistique).

## Problématique terrain
Lors des pics de commandes (promotions, opérations commerciales, cumuls de fin/début de semaine), le volume d'activité peut dépasser la capacité disponible de l'équipe présente. Si les besoins en renforts (intérimaires) ne sont pas anticipés en amont, les commandes s'accumulent en fin de journée et le pilotage devient plus réactif que prévisionnel.

## Approche Data
À partir d'un jeu de données simulé sur 75 jours d'activité :
1. **Estimation de la charge (en heures) :** prise en compte du volume de commandes, du nombre moyen d'articles par commande, d'un temps unitaire de préparation et d'une marge d'aléas.
2. **Comparaison charge vs capacité :** calcul des heures disponibles selon l'effectif présent et repérage des journées en surcharge.
3. **Aide au dimensionnement :** estimation du nombre de préparateurs recommandé (avec marge de sécurité) et du renfort à prévoir.

## Résultats visuels
- `outputs/charge_vs_capacite.png` : comparaison entre la charge de préparation requise et la capacité actuelle de l'équipe, avec mise en évidence des périodes de surcharge.
- `outputs/renforts_recommandes.png` : estimation du nombre de préparateurs supplémentaires à prévoir lors des journées critiques.

## Pistes d'évolution en alternance
- Brancher le script sur des historiques réels de commandes et de productivité (nettoyage, automatisation, détection d'anomalies).
- Affiner les temps standards par typologie de commande/produit et par créneau horaire.
- Déployer un tableau de bord de suivi clair (Excel / Power BI / Python) pour aider à l'anticipation des plannings et au suivi de production.