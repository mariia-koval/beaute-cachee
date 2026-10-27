# Beauté Cachée — Ventes & expérience client

**Étude de cas Data Analyst · Python · Sales & CRM · Customer Experience**

Beauté Cachée est une marque fictive de lingerie premium. Ce projet explore les attentes exprimées dans des avis clients et analyse une activité commerciale simulée pour dégager des pistes d’amélioration du produit et du service.

## Questions métier

- Quelles familles de produits sont les mieux évaluées et recommandées ?
- Quels problèmes ressortent des commentaires négatifs ?
- Comment évoluent les ventes et quels canaux et produits y contribuent ?
- Quels motifs de contact s’accompagnent de délais de traitement plus longs ?
- Comment la satisfaction du service varie-t-elle selon les délais ?

## Données

| Source | Contenu | Périmètre après nettoyage |
|---|---|---|
| Womens Clothing E-Commerce Reviews | Avis réels de vêtements féminins : notes, recommandations et commentaires | 23 485 avis |
| Sales / CRM synthétique | Clients, produits, commandes, lignes de commande, tickets et enquêtes de satisfaction | 6 tables, 33 000 lignes ; activité commerciale simulée de 2025 |

**Source des avis clients :** [Women’s E-Commerce Clothing Reviews](https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews), publié par **nicapotato** sur Kaggle.

Les données Sales / CRM sont synthétiques et ont été générées pour cette étude de cas.

Les deux sources sont analysées séparément : aucun lien individuel n’est établi entre les avis réels et les clients fictifs du CRM. Les avis concernent des vêtements féminins, pas exclusivement de la lingerie.

## Travail réalisé

1. Exploration de la structure et de la qualité des données.
2. Nettoyage des doublons, harmonisation des catégories, conversion des dates et contrôles de cohérence entre les tables.
3. Calcul des indicateurs Sales, CRM et avis clients avec des périmètres explicites.
4. Analyse des commentaires par expressions et règles thématiques, affinées après lecture d’exemples.
5. Comparaisons par famille de produits, âge, mois, canal de vente et motif de contact.
6. Synthèse des constats et recommandations dans une présentation métier.

**Outils :** Python, pandas, NumPy, Matplotlib, scikit-learn, statsmodels, Jupyter Notebook et Excel pour la documentation.

## Principaux résultats

### Avis clients

- **Fit & Sizing** est le premier thème détecté : 596 commentaires, soit **25,15 %** des 2 370 avis négatifs avec texte.
- Les règles identifient au moins un thème dans **33,42 %** des avis négatifs avec texte. Plusieurs thèmes peuvent apparaître dans un même avis.
- Le département **Bottoms** obtient une note moyenne de **4,29/5** et un taux de recommandation de **85,12 %**.
- **303 avis** présentent une divergence entre note et recommandation, ce qui invite à lire ces indicateurs ensemble.

### Ventes et service client — simulation 2025

| Indicateur | Résultat |
|---|---:|
| Montant net des ventes | 1 852 627 € |
| Commandes non annulées | 9 635 |
| Panier moyen | 192,28 € |
| Taux de réachat | 67,05 % |
| Clients dans la base | 5 000 |
| Tickets | 2 000 |
| Satisfaction du service — CSAT | 77,61 % |
| Délai moyen de première réponse | 9,13 h |
| Délai moyen de résolution | 27,34 h |
| Respect des délais de service — SLA | 69,43 % |

Les ventes sont calculées après remises et remboursements, taxes incluses et hors livraison, sur les commandes non annulées. Le réachat correspond à 2 776 clients ayant passé au moins deux commandes parmi 4 140 acheteurs. Le CSAT porte sur 795 réponses valides. Le SLA combine une réponse en 12 h maximum et une résolution en 48 h maximum, en heures calendaires, sur 1 966 tickets évaluables.

## Pistes d’action

- Préciser les informations sur les tailles, la coupe et les matières à partir des difficultés exprimées dans les avis.
- Préparer les périodes de forte activité : novembre et décembre représentent **26,7 %** des ventes annuelles simulées.
- Examiner le traitement des retours et remboursements : **51,02 h** de résolution moyenne et **47,38 %** de respect du SLA pour ce motif.

Ces recommandations découlent d’une analyse descriptive. Les relations observées ne démontrent pas de causalité et aucun effet des actions proposées n’a été mesuré.

## Organisation des fichiers

| Dossier | Contenu |
|---|---|
| 01_Data | Données originales (`raw`) et données nettoyées (`processed`) |
| 02_Notebooks | Les deux analyses Python avec leurs résultats enregistrés |
| 03_Documentation | Business Case, Data Documentation et schéma du projet |
| 05_Presentations | Synthèse métier en PDF et PowerPoint |

Pour une lecture rapide, commencer par la présentation PDF. Les notebooks détaillent les traitements ; le classeur Excel décrit les champs, les décisions de nettoyage et les calculs des KPI.

## Consulter ou reproduire l’analyse

Les résultats enregistrés peuvent être consultés dans les notebooks sans relancer les calculs.

Pour les exécuter localement :

1. Télécharger le projet et conserver son arborescence.
2. Installer les bibliothèques nécessaires dans un environnement Python :

   ```bash
   pip install jupyter pandas numpy matplotlib scikit-learn statsmodels
   ```

3. Vérifier les chemins des fichiers sources attendus par le code :
   - Avis : `01_Data/raw/Womens Clothing E-Commerce Reviews.csv`
   - Sales / CRM : les six CSV dans `01_Data/raw/Beaute_Cachee_Sales_CRM/raw/`
4. Ouvrir les notebooks depuis `02_Notebooks`, puis redémarrer le noyau et exécuter toutes les cellules :
   - `01_Beaute_Cachee_Data_Profiling.ipynb`
   - `02_Sales_CRM_Analysis.ipynb`

Les notebooks lisent les fichiers locaux : s’ils ne sont pas inclus dans le dépôt, ils doivent être placés aux emplacements indiqués avant l’exécution.

## Autrice

**Mariia Koval** — Data Analysis · Business Analysis · Expérience client

[LinkedIn](https://www.linkedin.com/in/mariia-v-koval/)
