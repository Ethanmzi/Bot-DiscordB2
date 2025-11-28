# Projet Bot Discord – B2 Informatique

## 1. Description générale

Ce projet est un **bot Discord** réalisé dans le cadre du rattrapage de B2.

Objectifs principaux du sujet :

- ✅ Implémenter un **historique des commandes** avec des **structures de données faites à la main** (liste chaînée / pile).
- ✅ Créer un **système de discussion** basé sur un **arbre** (questionnaire interactif).
- ✅ Mettre en place une **sauvegarde persistante** des données (fichier JSON).
- ✅ Ajouter au moins **3 fonctionnalités supplémentaires** au choix.

Le bot utilise la librairie Python **`discord.py`** et fonctionne avec un préfixe de commandes : `!`.

Le thème de la discussion :  
> Le bot aide l’utilisateur à **choisir un langage de programmation** à apprendre en fonction de son niveau et de ses préférences.

---

## 2. Installation et lancement

### 2.1. Prérequis

- Python 3.10+ installé.
- Un compte Discord.
- Un serveur Discord sur lequel vous pouvez inviter un bot.
- Un bot créé sur le **Discord Developer Portal**.

### 2.2. Installation des dépendances

Dans le dossier du projet (là où se trouve `main.py`) :

```bash
pip install -U "discord.py"
