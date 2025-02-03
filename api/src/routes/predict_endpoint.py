from fastapi import APIRouter, File, UploadFile
from PIL import Image
import mlflow
from routes.predict_models import PredictionResult, PredictionResultItem
import io
import numpy as np
import os


mlops_server_uri = os.environ.get('MLOPS_SERVER_URI')
model_path_binaire = os.environ.get('MODEL_PATH_BINAIRE')
model_path_multi = os.environ.get('MODEL_PATH_MULTI7')

mlflow.set_tracking_uri(mlops_server_uri)
binary_model = mlflow.pyfunc.load_model(model_path_binaire)
multi_class_model = mlflow.pyfunc.load_model(model_path_multi)

binary_class_names = ["Disease",
                      "Healthy"]
multi_class_names = ["Chest changes", 
                     "Degenerative infectious diseases", 
                     "Encapsulated lesions", 
                     "Higher density",
                     "Lower density", 
                     "Mediastinal changes", 
                     "Obstructive pulmonary diseases"]

router = APIRouter()

@router.post("/predict", 
             response_model=PredictionResult,
             tags=["Predictions"],
             description="Predict if the X-ray image has a pathology, and if yes predicts which one (among 7 pathologies).")
async def predict(
    file: UploadFile = File(..., 
                            description="Upload the X-ray image file here (png or jpg).", 
                            title="X-ray Image File", 
                            include_in_schema=False)):
    """Predict if the X-ray image has a pathology, and if yes predicts which one (among 7 pathologies).

    Args:
        file: X-ray image file.

    Returns:
        PredictionResult: Result of the prediction
    """
    contents = await file.read()
    binary_image = Image.open(io.BytesIO(contents)).convert('L')
    binary_image = binary_image.resize((224, 224))
    binary_image_array = np.array(binary_image)
    binary_image_array = binary_image_array / 255.0
    binary_image_array = np.expand_dims(binary_image_array, axis=0)
    binary_prediction = binary_model.predict(binary_image_array)
    binary_prediction_class = np.argmax(binary_prediction) 
    binary_prediction_class_name = binary_class_names[binary_prediction_class]
    if binary_prediction_class_name == 'Healthy':
        ranking = sorted(
            [PredictionResultItem(name=binary_class_names[i], 
                                  ratio=conf * 100,
                                  displayed_ratio=f'{round(float(conf * 100), 1)} %') for i, conf in enumerate(binary_prediction[0])],
            key=lambda x: x.Ratio,
            reverse=True
        )
        result = PredictionResult(
            has_pathology= False,
            prediction=PredictionResultItem(name=binary_prediction_class_name, 
                                            ratio=binary_prediction[0][binary_prediction_class]*100, 
                                            displayed_ratio=f'{round(binary_prediction[0][binary_prediction_class]*100, 1)} %'),
            ranking=ranking
        )
    else:
        multi_image = Image.open(io.BytesIO(contents)).convert('L')
        multi_image = multi_image.resize((224, 224))
        multi_image_array = np.array(multi_image)
        multi_image_array = multi_image_array / 255.0
        multi_image_array = np.expand_dims(multi_image_array, axis=0)
        multi_prediction = multi_class_model.predict(multi_image_array)
        multi_prediction_class = np.argmax(multi_prediction) 
        multi_prediction_class_name = multi_class_names[multi_prediction_class]
        ranking = sorted(
            [PredictionResultItem(name=multi_class_names[i], 
                                  ratio=conf * 100, 
                                  displayed_ratio=f'{round(float(conf * 100), 1)} %') for i, conf in enumerate(multi_prediction[0])],
            key=lambda x: x.Ratio,
            reverse=True
        )
        result = PredictionResult(
            has_pathology=True,
            prediction=PredictionResultItem(name=multi_prediction_class_name, 
                                            ratio=multi_prediction[0][multi_prediction_class]*100, 
                                            displayed_ratio=f'{round(multi_prediction[0][multi_prediction_class]*100, 1)} %'),
            ranking=ranking
        )
    return result