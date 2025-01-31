
# Application PulmoAId

## Prérequis

Vérifier que l'environnement virtuel Python du dépôt est correctement installé et activé en consultant la ([documentation d'installation](../README.md#installation)).

Créer le fichier **.env** dans le dossier **app** et définir les valeurs suivantes :

```
DEFAULT_PORT=7860                                                         # Port par défaut de streamlit
PORT=6002                                                                 # Port de l'application
API_BASE_URL=https://david-rem-jedha-final-project-api.hf.space/api/v1    # Url de base de l'API
```

## Exécution

### Exécution locale

Exécuter les commandes suivantes. L'application est accessible via http://localhost:6002.

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

L'application est déployée sur Hugging à cette adresse : https://david-rem-jedha-final-project-app.hf.space

### Procédure de déploiement

- Créer un espace nommé **jeadha-final-project-app** dans Huggingface
- Dans l'onglet *Files*, ajouter les éléments suivants :
  - Dockerfile
  - requirements.txt
  - src
- Committer les modifications sur la branche *main*
- Dans l'onglet Settings, ajouter les secrets suivants :
  - DEFAULT_PORT : 7860
  - PORT : 7860
- Accéder à l'onglet *App* et vérifier que l'application a correctement démarré.