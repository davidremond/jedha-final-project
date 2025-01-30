from pydantic import BaseModel, Field
from typing import List, Literal, Dict

class SimilarXRaysResult(BaseModel):
    """
    Similary XRay result
    """
        
    Samples : Dict[str, List[str]] = Field(
        alias="samples", 
        description="List of sample images by pathology.", 
        example=[
            {"Normal": ['images/Normal/img1.png', 'images/Normal/img2.png', 'images/Normal/img3.png' ]}, 
            {"Chest_Changes": ['images/Chest_Changes/img1.png', 'images/Chest_Changes/img2.png', 'images/Chest_Changes/img3.png' ]}, 
            ]
        )
