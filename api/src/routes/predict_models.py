from pydantic import BaseModel, Field
from typing import List, Literal

class PredictionResultItem(BaseModel):
    """
    Pathology result.
    """
    Name: Literal["Chest changes", 
                  "Degenerative infectious diseases", 
                  "Encapsulated lesions", 
                  "Higher density",
                  "Lower density", 
                  "Mediastinal changes", 
                  "Obstructive pulmonary diseases",
                  "Disease",
                  "Healthy"] = Field(
                      alias="name", 
                      description="Name of the prediction.", 
                      example="Obstructive pulmonary diseases"
                      )
    Ratio : float = Field(
        alias="ratio", 
        ge=0, 
        le=100, 
        description="Confidence percentage of the prediction.", 
        example=65.643543
        )
    DisplayedRatio : str = Field(
        alias="displayed_ratio",
        description="Displayed confidence percentage of the prediction.",
        example="65.6 %"
        )

class PredictionResult(BaseModel):
    """
    Prediction result.
    """
    HasPathology: bool = Field(
        alias="has_pathology", 
        description="Indicates if a pathology has been detected.", 
        example=True
        )
    Prediction : PredictionResultItem = Field(
        alias="prediction", 
        description="Prediction result.", 
        example={"name": "Obstructive pulmonary diseases", "ratio": 65.643543, "displayed_ratio": "65.6 %"}
        )
    Ranking : List[PredictionResultItem] = Field(
        alias="ranking", 
        description="Ranking of the detection.", 
        example=[
            {"name": "Obstructive pulmonary diseases", "ratio": 65.643543, "displayed_ratio": "65.6 %"}, 
            {"name": "Chest changes", "ratio": 45.6455783, "displayed_ratio": "45.6 %"}, 
            {"name": "Degenerative infectious diseases", "ratio": 35.6345345, "displayed_ratio": "35.6 %"}, 
            {"name": "Encapsulated lesions", "ratio": 25.6123123, "displayed_ratio": "25.6 %"}, 
            {"name": "Higher density", "ratio": 15.608656, "displayed_ratio": "15.6 %"}, 
            {"name": "Lower density", "ratio": 5.6234245, "displayed_ratio": "5.6 %"}, 
            {"name": "Mediastinal changes", "ratio": 0.6345676, "displayed_ratio": "0.6 %"}
            ]
        )