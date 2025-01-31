
# API PulmoAId

## Prérequis

Vérifier que l'environnement virtuel Python du dépôt est correctement installé et activé en consultant la ([documentation d'installation](../README.md#installation)).

Créer le fichier **.env** dans le dossier **api** et définir les valeurs suivantes :

```
DEFAULT_PORT=80                                                      # Port par défaut du serveur web FastAPI
PORT=6001                                                            # Port de l'application
MLOPS_SERVER_URI=https://******-jedha-final-project-mlops.hf.space   # URL du serveur MLOPS
MODEL_PATH=models:/lung_8_classes/1                                  # Chemin du modèle 8 classes
MODEL_PATH_BINAIRE=models:/lung_2_classes/2                          # Chemin du modèle de classification binaire
MODEL_PATH_MULTI7=models:/lung_7_classes/2                           # Chemin du modèle 7 classes
```

## Exécution

### Exécution locale

Exécuter les commandes suivantes. L'application est accessible via http://localhost:6001.

**Windows**

```
cd app
.\run_local_app.ps1
```

**Linux/Mac**

```
cd app
sh run_local_app.sh
```

### Exécution avec Docker

Ces scripts sont utilisés pour mettre au point les images Docker en local avant déploiement sur un hébergement distant.

**Windows**

```
cd app
.\run_local_server.ps1
```

**Linux/Mac**

```
cd app
sh run_local_server.sh
```

## Déploiement en production

### Accès

L'application est déployée sur Hugging à cette adresse : https://david-rem-jedha-final-project-api.hf.space

### Documentation

La documentation est disponible à cette adresse : https://david-rem-jedha-final-project-api.hf.space/docs

### Procédure de déploiement

- Créer un espace nommé **jeadha-final-project-api** dans Huggingface
- Dans l'onglet *Files*, ajouter les éléments suivants :
  - Dockerfile
  - requirements.txt
  - src
- Committer les modifications sur la branche *main*
- Dans l'onglet Settings, ajouter les secrets suivants :
  - DEFAULT_PORT : 7860
  - PORT : 7860
  - MLOPS_SERVER_URI : https://david-rem-jedha-final-project-mlops.hf.space
  - MODEL_PATH : models:/lung_8_classes/1
  - MODEL_PATH_BINAIRE : models:/lung_2_classes/1
  - MODEL_PATH_MULTI7 : models:/lung_7_classes/1
- Accéder à l'onglet *App* et vérifier que l'application a correctement démarré.