#!/bin/bash

envFilePath=".env"

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

echo "MODEL_PATH=$MODEL_PATH"

# Exécuter la commande FastAPI
fastapi run src/app.py --host localhost --reload