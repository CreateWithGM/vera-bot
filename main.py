from fastapi import FastAPI
from bot import compose

app = FastAPI()

@app.get("/v1/healthz")
def health():
    return {"status": "ok"}

@app.get("/v1/metadata")
def metadata():
    return {"bot": "vera-compose-engine", "version": "1.0"}

@app.post("/v1/context")
def context(data: dict):
    return {"accepted": True}

@app.post("/v1/tick")
def tick(data: dict):
    return {"status": "processed"}

@app.post("/v1/reply")
def reply(data: dict):
    return compose(
        data["category"],
        data["merchant"],
        data["trigger"],
        data.get("customer")
    )