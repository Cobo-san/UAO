"""
FastAPI / Microservice Web App Template
Account Target: sounddharma@gmail.com
"""

from fastapi import FastAPI

app = FastAPI(title="Sounddharma Microservice", version="1.0.0")

@app.get("/")
def read_root():
    return {"status": "HEALTHY", "account": "sounddharma@gmail.com"}
