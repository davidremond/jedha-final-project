import os
from fastapi import APIRouter, HTTPException, Query
from typing import Annotated, List
from pydantic import Field
from routes.samplesModels import SimilarXRaysResult

router = APIRouter()

# Dictionnaire de correspondance entre les classes et les dossiers d'images
class_to_folder_images = {
    "Chest changes": "images/Chest_Changes/",
    "Degenerative infectious diseases": "images/Degenerative_Infectious_Diseases/",
    "Encapsulated lesions": "images/Encapsulated_Lesions/",
    "Higher density": "images/Higher_Density/",
    "Lower density": "images/Lower_Density/",
    "Mediastinal changes": "images/Mediastinal_Changes/",
    "Normal": "images/Normal/",
    "Obstructive pulmonary diseases": "images/Obstructive_Pulmonary_Diseases/"
}

@router.get("/similar_xrays", response_model=SimilarXRaysResult)
async def similar_xrays(class_names: Annotated[List[str], Query()] ):
    """
    Récupère la liste des images pour une classe donnée.
    """
    
    samples ={}
    
    # Chemin du dossier associé à la classe
    for class_name in class_names:
        print(class_name)
        print("folder_path : ", class_to_folder_images[class_name])
        folder_path = class_to_folder_images[class_name]
        print(folder_path)
        print(os.getcwd())
        
        # Vérifier si le dossier existe
        if not os.path.exists(folder_path):
            raise HTTPException(status_code=500, detail=f"Le dossier pour la classe '{class_name}' n'existe pas.")

        # Obtenir la liste des fichiers dans le dossier
        images = [img for img in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, img))]

        samples[class_name] = images
    result = SimilarXRaysResult(samples=samples)    
    print("ici",result)    
    return result

#images\Chest_Changes\image_0066.jpg