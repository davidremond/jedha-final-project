from pydantic import BaseModel, Field
from typing import List, Dict

class SimilarXRaysResult(BaseModel):
    """
    Similary XRay result.
    """
        
    Samples : Dict[str, List[str]] = Field(
        alias="samples", 
        description="List of sample images by pathology.", 
        example=[
            {"Normal": ['/9j/4AAQSZ....', '/9j/4AAkZJ...', '/9j/4AAQSk...' ]}, 
            {"Chest_Changes": ['/9j/4AAQSZ....', '/9j/4AAkZJ...', '/9j/4AAQSk...' ]}
            ]
        )
