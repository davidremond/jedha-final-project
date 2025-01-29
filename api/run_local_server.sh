#!/bin/bash

envFilePath=".env"

# Lire le fichier .env et exporter les variables d'environnement
while IFS='=' read -r key value; do
    # Ignorer les lignes vides et les commentaires
    if [ -z "$key" ] || [[ "$key" =~ ^\s*# ]]; then
        continue
    fi

    # Supprimer les espaces en début et fin de chaîne
    key=$(echo "$key" | xargs)
    value=$(echo "$value" | xargs)

    # Exporter la variable d'environnement
    export "$key=$value"
done < "$envFilePath"

# Supprimer le conteneur Docker s'il existe
docker rm jedha-final-project-api -f

# Supprimer l'image Docker s'il existe
docker image rm jedha-final-project-api

# Construire l'image Docker
docker build . -t jedha-final-project-api

# Exécuter le conteneur Docker
docker run --name jedha-final-project-api \
    --detach \
    --volume ./src:/app \
    --env DEFAULT_PORT="$DEFAULT_PORT" \
    --env MLOPS_SERVER_URI="$MLOPS_SERVER_URI" \
    --env MODEL_PATH="$MODEL_PATH" \
    --publish "$PORT:$DEFAULT_PORT" \
    jedha-final-project-api