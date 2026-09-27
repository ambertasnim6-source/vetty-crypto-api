from fastapi import FastAPI

app = FastAPI(
    title="Vetty Crypto API",
    version="1.0.0",
    description="REST API for cryptocurrency market data.",
)


@app.get("/")
async def root():
    return {
        "message": "Vetty Crypto API is running",
        "version": "1.0.0",
    }