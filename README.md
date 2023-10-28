# Projet de Web Scrapping

## Objectif 🎯

Créer des outils modulables et réutilisables pour l'extraction de données. Ces outils sont optimisés grâce à la parallélisation des requêtes et fournissent un retour visuel de la progression avec une barre personnalisée « 🚀 » ce petit détail se révélera amusant lors de l'extraction.

> 🔔 **Note Ethique et Juridique** :  Le web scrapping opère dans une zone éthique et juridique parfois floue. Il est essentiel de mentionner que pour ce projet, les directives du fichier robots.txt ont été suivies pour tous les exemples d'extraction fournis.

## Détails des Extractions 🚀

### 1. Extraction F1 🏎️

- **Objectif** : Récupérer tous les résultats des Grands Prix de F1 de 1950 à aujourd'hui.
  
- **Étapes** :
  1. Extraire les URLs pour chaque année.
  2. À partir des URLs annuelles, extraire les URLs de chaque course.
  3. Normaliser, concaténer les données et exporter en CSV.

### 2. Extraction CPU 💾

- **Objectif** : Constituer 5 bases de données pour un classement de composants d'ordinateurs et des données de benchmarks (RAM DDR4 et DDR5, SSD, Carte graphique, Processeur).

- **Étapes** :
  1. Extraire le classement général.
  2. Extraire les liens de chaque composant pour des données de benchmark détaillées.
  3. Créer une seconde table à partir de ces données.
  4. Fusionner les tables.

### 3. Extraction via l'API Castorama France 🏡

- **Objectif** : Interroger l'API de Castorama France pour obtenir un catalogue détaillé des produits.

- **Étapes** :
  1. Identifier et collecter les variables de requête du site web de Castorama.
  2. Interroger l'API pour différentes catégories de produits et récupérer les données.
  3. Stocker les données au format JSON.

> ✨ **Résultat Impressionnant** : Un fichier JSON de 10 millions de lignes obtenu en moins de 5 minutes!

---
