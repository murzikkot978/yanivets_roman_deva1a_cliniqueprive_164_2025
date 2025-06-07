# 🏥 Projet de Gestion Médicale (Python + MAMP + MySQL)

Ce projet est une application de gestion médicale développée en **Python**, utilisant une base de données **MySQL** via **MAMP**. Il permet de gérer les **médecins**, **patients**, **consultations**, **spécialités** et **factures**.

---

## 📁 Tables de la base de données

- `t_medecin`
- `t_patient`
- `t_consultation`
- `t_specialite`
- `t_facture`

---

## ⚙️ Fonctionnalités

- Ajouter, modifier et supprimer les **médecins**
- Ajouter, modifier et supprimer les **patients**
- Gérer les **consultations**
- Lier les **médecins** à leurs **spécialités**
- Gérer les **factures** liées aux consultations

---

## 🧰 Technologies utilisées

- Python 3
- MySQL via **MAMP**
- Bibliothèques : `mysql-connector-python`, `tkinter` (si interface graphique)

---

## 🛠️ INSTALLATION DU PROJET

### ✅ Prérequis

- Python 3 installé → [https://www.python.org/downloads/](https://www.python.org/downloads/)
- MAMP installé → [https://www.mamp.info/en/](https://www.mamp.info/en/)
- Git (optionnel, pour cloner le projet)

---

### 🧑‍💻 Installation rapide en terminal (Bash)

```bash
# Étape 1 - Cloner le projet
git clone https://github.com/murzikkot978/yanivets_roman_deva1a_cliniqueprive_164_2025.git
cd votre-projet

# Étape 2 - Installer les bibliothèques Python nécessaires
pip install mysql-connector-python

# Étape 3 - Démarrer les serveurs via MAMP (manuellement)
# Lancez l'application MAMP
# Cliquez sur "Start Servers"

# Étape 4 - Accéder à phpMyAdmin
# Ouvrez votre navigateur et allez à :
# http://localhost/phpMyAdmin/

# Étape 5 - Créer la base de données
# Créez une base appelée : gestion_medicale

# Étape 6 - Importer le fichier SQL
# Cliquez sur "gestion_medicale" > "Importer"
# Importez le fichier : database.sql (inclus dans le projet)

# Étape 7 - Vérifier la configuration de la base de données
# Fichier : config.py
# Exemple :
# db_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': 'root',
#     'database': 'gestion_medicale'
# }

# Étape 8 - Lancer l'application
python main.py
