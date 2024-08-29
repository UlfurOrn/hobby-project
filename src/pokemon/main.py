import uvicorn
from fastapi import FastAPI

app = FastAPI(host="127.0.0.1", port=8000)

if __name__ == "__main__":
    uvicorn.run(app)
