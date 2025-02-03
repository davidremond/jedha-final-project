import os
import base64
from fastapi import APIRouter, HTTPException, Query
from typing import Annotated, List
from routes.similar_xrays_models import SimilarXRaysResult

router = APIRouter()

@router.get("/similar_xrays", 
            response_model=SimilarXRaysResult,
            tags=["Repository"],
            description="Return sample x-rays images depending on requested class names.")
async def similar_xrays(class_names: Annotated[List[str], Query()] ):
    """Return sample x-rays images depending on requested class names.
    
        Args:
        class_names: Array of class names.

    Returns:
        SimilarXRaysResult: Result that contains 3 sample images for each requested class name. 
    """
    samples ={}
    root_folder = os.getcwd()
    subdir = os.listdir(root_folder)
    if subdir.count('src') == 1:
        root_folder = os.path.join(root_folder, 'src')
    for class_name in class_names:
        folder_path = os.path.join(root_folder, f'samples/{class_name.lower().replace(' ', '_')}')
        if not os.path.exists(folder_path):
            raise HTTPException(status_code=500, detail=f"Le dossier pour la classe '{class_name}' n'existe pas.")
        images = []
        files_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        for img in files_list:
            with open(os.path.join(folder_path, img), 'rb') as file:
                images.append(base64.b64encode(file.read()).decode('utf-8'))
        samples[class_name] = images
    result = SimilarXRaysResult(samples=samples)    
    return result