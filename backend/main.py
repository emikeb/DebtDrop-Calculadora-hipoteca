from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import MortgageRequest, MortgageResponse
from services import MortgageCalculator

app = FastAPI(title="Calculadora Hipotecaria API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/calcular", response_model=MortgageResponse)
def calcular_hipoteca(request: MortgageRequest):
    calculator = MortgageCalculator(request)
    return calculator.calculate()
