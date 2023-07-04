from fastapi import FastAPI

app = FastAPI()


@app.get("/api/test")
async def root():
    return {
        "message": "fast api app",
        "service": "v1"
    }
