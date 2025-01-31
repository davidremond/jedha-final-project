# une prediction binaire malade/sain puis si malade une prediction à 7 classes
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

# vérifier si 0 et 1 ok après data augmentation
class_names_binaire = ["Disease", "Healthy"]
class_names_multi = ["Chest changes", "Degenerative infectious diseases", "Encapsulated lesions", "Higher density",
               "Lower density", "Mediastinal changes", "Obstructive pulmonary diseases"]

router = APIRouter()

@router.post("/predict", 
             response_model=PredictionResult,
             description="Predict if the X-ray image has a pathology, and if yes predicts which one (among 7 pathologies).")
async def predict(
    file: UploadFile = File(..., description="Upload the X-ray image file here (png or jpg).", title="X-ray Image File", include_in_schema=False)):
    contents = await file.read()

    

    image_binaire = Image.open(io.BytesIO(contents)).convert('RGB')
    image_multi = Image.open(io.BytesIO(contents)) 
    # à refaire : une unique taille d'image, pour tous les modeles : on se met en size (224,224)
    image_binaire = image_binaire.resize((128, 128)) #si modele final = VGG19, mettre : (224,224)
    image_binaire_array = np.array(image_binaire)
    image_binaire_array = image_binaire_array / 255.0
    image_binaire_array = np.expand_dims(image_binaire_array, axis=0)
    image_multi = image_multi.resize((128,128))
    image_multi_array = np.array(image_multi)
    image_multi_array = image_multi_array / 255.0
    image_multi_array = np.expand_dims(image_multi_array, axis=0)

    prediction_binaire = binary_model.predict(image_binaire_array)
    predicted_binaire_class = np.argmax(prediction_binaire) 
    class_binaire_name = class_names_binaire[predicted_binaire_class]

    if class_binaire_name == 'Healthy':
        ranking = sorted(
            [PredictionResultItem(name=class_names_binaire[i], ratio=conf * 100, displayed_ratio=f'{round(float(conf * 100), 1)} %') for i, conf in enumerate(prediction_binaire[0])],
            key=lambda x: x.Ratio,
            reverse=True
        )
        print("round=",round(prediction_binaire[0][predicted_binaire_class]*100, 1))
        result = PredictionResult(
            has_pathology= False,
            prediction=PredictionResultItem(name=class_binaire_name, ratio=prediction_binaire[0][predicted_binaire_class]*100, displayed_ratio=f'{round(prediction_binaire[0][predicted_binaire_class]*100, 1)} %'),
            ranking=ranking
        )

    else:
        prediction_multi = multi_class_model.predict(image_multi_array)
        predicted_multi_class = np.argmax(prediction_multi) 
        class_multi_name = class_names_multi[predicted_multi_class]
        ranking = sorted(
            [PredictionResultItem(name=class_names_multi[i], ratio=conf * 100, displayed_ratio=f'{round(float(conf * 100), 1)} %') for i, conf in enumerate(prediction_multi[0])],
            key=lambda x: x.Ratio,
            reverse=True
        )
        print("round=",round(prediction_multi[0][predicted_multi_class]*100, 1))
        result = PredictionResult(
            has_pathology=True,
            prediction=PredictionResultItem(name=class_multi_name, ratio=prediction_multi[0][predicted_multi_class]*100, displayed_ratio=f'{round(prediction_multi[0][predicted_multi_class]*100, 1)} %'),
            ranking=ranking
        )

    return result