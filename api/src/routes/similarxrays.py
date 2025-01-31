import os
import base64
from fastapi import APIRouter, HTTPException, Query
from typing import Annotated, List
from pydantic import Field
from routes.similarxraysModels import SimilarXRaysResult

router = APIRouter()

@router.get("/similar_xrays", response_model=SimilarXRaysResult)
async def similar_xrays(class_names: Annotated[List[str], Query()] ):
    """
    Récupère la liste des images pour une classe donnée.
    """
    samples ={}
    
    # Chemin du dossier associé à la classe
    root_folder = os.getcwd()
    subdir = os.listdir(root_folder)
    if subdir.count('src') == 1:
        root_folder = os.path.join(root_folder, 'src')

    for class_name in class_names:
        folder_path = os.path.join(root_folder, f'images/{class_name.lower().replace(' ', '_')}')
        # Vérifier si le dossier existe
        if not os.path.exists(folder_path):
            raise HTTPException(status_code=500, detail=f"Le dossier pour la classe '{class_name}' n'existe pas.")

        # Obtenir la liste des fichiers dans le dossier
        images = []
        print("folder_path=",folder_path)
        files_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        for img in files_list:
            print("img=",img)
            with open(os.path.join(folder_path, img), 'rb') as file:
                images.append(base64.b64encode(file.read()).decode('utf-8'))

        samples[class_name] = images

    result = SimilarXRaysResult(samples=samples)    
    return result