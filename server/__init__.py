from fastapi import FastAPI
from uvicorn import Server as UvicornServer, Config
app = FastAPI()
 
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}
server = UvicornServer (
    Config (
        app=app,
        host="0.0.0.0",
        port=8080
    )
)
