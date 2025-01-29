# Application de prédiction

## Prérequis

Vérifier que l'environnement virtuel Python du dépôt est correctement installé en consultant la ([documentation d'installation](../README.md#installation)).

Créer le fichier **.env** dans le dossier **app** et définir les valeurs suivantes :

```
DEFAULT_PORT=7860 # Port par défaut de streamlit
PORT=6002 # Port de l'application
```

## Exécution locale

**Windows**

Exécuter le fichier [run_local_app.ps1](run_local_app.ps1).

**Linux/Mac**

Exécuter le fichier [run_local_app.sh](run_local_app.sh).

## Exécution avec Docker

**Windows**

Exécuter le fichier [run_local_server.ps1](run_local_server.ps1).

**Linux/Mac**

Exécuter le fichier [run_local_server.sh](run_local_server.sh).

## Déploiement sur Huggingface

L'application est déployée sur Hugging à cette adresse : https://david-rem-jedha-final-project-app.hf.space
