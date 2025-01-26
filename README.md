# MoteurFusionMultimodale

Reproduction de l'application de dessin multimodale présenté dans le projet.

TACHES POSSIBLES :

* Créer une forme
* Déplacer une forme
* Supprimer forme

Formes possibles :

* rectangle
* cercle
* losange
* triangle

couleurs possibles :

* rouge
* vert
* bleu
* jaune
* orange

## Description

Ce projet est un moteur de fusion multimodale qui permet d'intégrer différentes sources de données pour une analyse approfondie.

## Dépendances

Pour installer les dépendances, utilisez le fichier `conda_env.yaml` fourni. Voici quelques-unes des dépendances principales :

* `dollarn`
* `pygame=2.6.1`
* `python=3.12.7`
* `numpy==2.1.3` (via `pip`)

## Installation

Pour installer les dépendances, exécutez la commande suivante :

```bash
conda env create -f conda_env.yaml
```

puis sourcer l'env :

```bash
conda activate ihm
```

## Utilisation

Pour utiliser le moteur, exécutez le script principal :

```bash
python main.py
python fusion_engine.py
.\sra5\sra5_on.bat
```

## Licence

Ce projet est sous licence GNU GPL v3. Voir le fichier `LICENSE` pour plus de détails.
