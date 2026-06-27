from fastapi import FastAPI
from solver import solve_supply_network

app = FastAPI(
    title="Supply Chain Network Design Optimization API",
    description="Operations Research project deployed on Microsoft Azure using FastAPI and OR-Tools.",
    version="1.0"
)

@app.get("/")
def home():
    return {
        "message": "Supply Chain Network Design Optimization API is running on Azure"
    }

@app.get("/solve")
def solve():
    return solve_supply_network()