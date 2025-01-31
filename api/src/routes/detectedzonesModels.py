from pydantic import BaseModel, Field
from typing import ByteString, List, Literal, Dict

class DetectedZonesResult(BaseModel):
    """
    Detected zones result
    """
        
    ImageWithDetectedZones : str = Field(
        alias="image_with_detected_zones", 
        description="Image with detected zones in base64 format.", 
        example='/9j/4AAQSZ....'
        )
