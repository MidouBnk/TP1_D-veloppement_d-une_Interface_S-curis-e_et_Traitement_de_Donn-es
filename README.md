## Comment lancer (How to Run)

**Ouvre un terminal** dans le dossier du projet.

**Installe les dépendances** :
```bash
pip install pandas numpy sqlalchemy matplotlib seaborn mysql-connector-python

Démarre MySQL via XAMPP.

Crée la base de données :
CREATE DATABASE tp_interface_data;

Importe le fichier SQL :
db.sql

Lance l’application :
python auth_app.py

Connexion ou inscription :
Utilise auth_app.py pour te connecter.
Si tu n’as pas encore de compte, ouvre register_app.py pour en créer un.
Après la connexion, l’interface principale (main_app.py) s’ouvre et permet le chargement, nettoyage et visualisation des données.


---

Souhaites-tu que je te fasse la même section mais **en français seulement** (sans “How to Run”) ?
