import os
from fastapi import APIRouter, Query
from typing import List, Optional

router = APIRouter()

# Dictionnaire de correspondance entre les classes et les dossiers d'images
class_to_folder_images = {
    "Chest changes": "iumages/Chest_Changes/",
    "Degenerative infectious diseases": "images/Degenerative_Infectious_Diseases/",
    "Encapsulated lesions": "images/Encapsulated_Lesions/",
    "Higher density": "images/Higher_Density/",
    "Lower density": "images/Lower_Density/",
    "Mediastinal changes": "images/Mediastinal_Changes/",
    "Normal": "images/Normal/",
    "Obstructive pulmonary diseases": "images/Obstructive_Pulmonary_Diseases/"
}

@router.get("/get_images_top_folders", description="Return all images from folders for classes with a configurable score threshold.")
async def get_top_folders(predictions: List[str] = Query(..., description="List of class names")):
    """
    predictions: List of class names ".
    Returns all images from folders for all classes.
    """
    # Convertir les prédictions en une liste de dictionnaires
    parsed_predictions = []
    for prediction in predictions:
        try:
            class_name, score = prediction.split(":")
            parsed_predictions.append({"class_name": class_name, "score": float(score)})
        except ValueError:
            continue
    
    # Filtrer les classes ayant un taux supérieur au seuil défini
    filtered_predictions = [pred for pred in parsed_predictions if pred['score'] > threshold]
    
    # Trier par score décroissant
    filtered_predictions.sort(key=lambda x: x['score'], reverse=True)
    
    # Récupérer toutes les images des dossiers correspondants
    top_folders = []
    for pred in filtered_predictions:
        folder_path = class_to_folder_images.get(pred["class_name"], "images/default/")
        try:
            images = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        except FileNotFoundError:
            images = []
        top_folders.append({"class": pred["class_name"], "folder": folder_path, "images": images})
    
    return {"top_folders": top_folders}