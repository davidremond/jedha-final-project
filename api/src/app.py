from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routes import detected_zones_endpoint, similar_xrays_endpoint, simple_predict_endpoint, predict_endpoint
import os
import uvicorn

default_port = os.environ.get('DEFAULT_PORT')

app = FastAPI(title="PulmoAId API", 
              version="1.0.0", 
              description="Fournit des services de prédiction de maladies pulmonaires à partir d'images radiologiques.")

@app.exception_handler(Exception)
async def global_exception_handler(_: Request, ex: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(ex)}
    )

app.include_router(simple_predict_endpoint.router, prefix="/api/v1")
app.include_router(predict_endpoint.router, prefix="/api/v1")
app.include_router(detected_zones_endpoint.router, prefix="/api/v1")
app.include_router(similar_xrays_endpoint.router, prefix="/api/v1")

if __name__=="__main__":
    uvicorn.run(app, host='localhost', port=default_port)