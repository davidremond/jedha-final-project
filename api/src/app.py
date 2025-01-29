from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routes import predict, zones, samples
import os
import uvicorn

default_port = os.environ.get('DEFAULT_PORT')

app = FastAPI(title="Assistance au diagnostic pulmonaire API", 
              version="1.0.0", 
              description="TODO")

@app.exception_handler(Exception)
async def global_exception_handler(_: Request, ex: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(ex)}
    )

app.include_router(predict.router, prefix="/api/v1")
app.include_router(zones.router, prefix="/api/v1")
app.include_router(samples.router, prefix="/api/v1")

if __name__=="__main__":
    uvicorn.run(app, host='localhost', port=default_port)