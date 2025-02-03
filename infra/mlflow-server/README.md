# Serveur MLFLOW

## Utilisation

Pour tracer les expérimentations, utiliser l'URL suivantes : https://david-rem-jedha-final-project-mlops.hf.space

## Déploiement

### Accès

Le serveur est déployé sur huggingface et accessible via cette URL : https://david-rem-jedha-final-project-mlops.hf.space

### Procédure de déploiement

Cette procédure ne doit pas être utilisée en production et est donnée pour un usage éducatif.

#### Sécurité

Créer un utilisateur jedha-final-project, lui créer une clé d'accès et lui attribuer les autorisations suivantes :
- AmazonS3FullAccess


#### Stockage AWS

Sélectionner la région la plus proche des utilisateurs (dans notre cas, eu-west-3).

Créer un stockage S3 sur AWS avec les paramètres suivants :
- Nom du compartiment : jedha-final-project
- Bloquer tous les accès publics : Non (et cocher la confirmation)

Créer une base de données sur AWS avec les paramètres suivants :
- Type de moteur : PostgreSQL
- Modèles : Offre gratuite
- Identifiant d'instance de base de données : jedha-final-project
- Mot de passe principal : **************
- Accès public : Oui
- Activer l'analyse des performances : Non

#### Serveur Huggingface

- Créer un espace nommé **jeadha-final-project-mlflow** dans Huggingface
- Dans l'onglet *Files*, ajouter les éléments suivants :
  - Dockerfile
  - requirements.txt
- Committer les modifications sur la branche *main*
- Dans l'onglet Settings, ajouter les secrets suivants :
  - DEFAULT_PORT : 7860
  - PORT : 7860
  - AWS_ACCESS_KEY_ID : **************
  - AWS_SECRET_ACCESS_KEY : **************
  - AWS_DEFAULT_REGION : eu-west-3
  - BACKEND_STORE_URI : postgresql://{user}:{password}@{endpoint}:{port}/{database_name}?sslmode=require
  - ARTIFACT_STORE_URI : s3://jedha-final-project
  - MLOPS_SERVER_PORT : 7860

- Accéder à l'onglet *App* et vérifier que l'application a correctement démarré.

> Le endpoint et le port de la base SQL sont affichés dans l'onglet Connectiivité et sécurité de l'instance RDS.