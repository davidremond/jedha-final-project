# une unique prediction à 8 classes

from fastapi import APIRouter, File, UploadFile
from PIL import Image
from utils.cache import load_model_cached
from routes.simple_predict_models import PredictionResult, PredictionResultItem
import io
import mlflow
import numpy as np
import os

model = load_model_cached(os.environ.get('MODEL_PATH'))

class_names = ["Chest changes", "Degenerative infectious diseases", "Encapsulated lesions", "Higher density",
               "Lower density", "Mediastinal changes", "Normal", "Obstructive pulmonary diseases"]
               
router = APIRouter()

@router.post("/simple_predict", 
             response_model=PredictionResult,
             description="Predict if the X-ray image has a pathology.")
async def simple_predict(
    file: UploadFile = File(..., description="Upload the X-ray image file here.", title="X-ray Image File", include_in_schema=False)):
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
    print("round=",round(prediction[0][predicted_class]*100, 1))
    result = PredictionResult(
        has_pathology=True if predicted_class != 6 else False,
        prediction=PredictionResultItem(name=class_name, ratio=prediction[0][predicted_class]*100, displayed_ratio=f'{round(prediction[0][predicted_class]*100, 1)} %'),
        ranking=ranking
    )
    
    return result