from fastapi import FastAPI

app = FastAPI()

@app.post("/messaging_api/handle_request")
async def handle_request():
    return "ok"