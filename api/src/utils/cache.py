from functools import lru_cache
import mlflow
import os

mlflow.set_tracking_uri(os.environ.get('MLOPS_SERVER_URI'))

model_cache = {}

@lru_cache()
def load_model_cached(model_path: str):
    if model_path in model_cache:
        print(f"Loading model {model_path} from cache")
        return model_cache[model_path]
    else:
        print(f"Loading model {model_path} from mlflow")
        model = mlflow.pyfunc.load_model(model_path)
        model_cache[model_path] = model
        return model