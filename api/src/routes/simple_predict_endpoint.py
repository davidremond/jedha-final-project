from fastapi import APIRouter, File, UploadFile
from PIL import Image
from routes.simple_predict_models import PredictionResult, PredictionResultItem
import io
import mlflow
import numpy as np
import os

mlops_server_uri = os.environ.get('MLOPS_SERVER_URI')
model_path = os.environ.get('MODEL_PATH')

mlflow.set_tracking_uri(mlops_server_uri)
model = mlflow.pyfunc.load_model(model_path)

class_names = ["Chest changes", 
               "Degenerative infectious diseases", 
               "Encapsulated lesions", 
               "Higher density",
               "Lower density", 
               "Mediastinal changes", 
               "Normal", 
               "Obstructive pulmonary diseases"]
               
router = APIRouter()

@router.post("/simple_predict", 
             response_model=PredictionResult,
             tags=["Predictions"],
             description="Predict if the X-ray image has a pathology.")
async def simple_predict(
    file: UploadFile = File(..., description="Upload the X-ray image file here.", title="X-ray Image File", include_in_schema=False)):
    """Predict if the X-ray image has a pathology.

    Args:
        file: X-ray image.

    Returns:
        PredictionResult: Result of the prediction.
    """
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    image = image.resize((256, 256))
    image_array = np.array(image)
    image_array = image_array / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    prediction = model.predict(image_array)
    predicted_class = np.argmax(prediction) 
    class_name = class_names[predicted_class]
    ranking = sorted(
        [PredictionResultItem(name=class_names[i], ratio=conf * 100, displayed_ratio=f'{round(float(conf * 100), 1)} %') for i, conf in enumerate(prediction[0])],
        key=lambda x: x.Ratio,
        reverse=True
    )
    result = PredictionResult(
        has_pathology=True if predicted_class != 6 else False,
        prediction=PredictionResultItem(name=class_name, ratio=prediction[0][predicted_class]*100, displayed_ratio=f'{round(prediction[0][predicted_class]*100, 1)} %'),
        ranking=ranking
    )    
    return result