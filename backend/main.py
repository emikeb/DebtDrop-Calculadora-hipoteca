from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import MortgageRequest, MortgageResponse
from services import calculate_mortgage

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
    cuota, intereses, total, amortizacion, cuota_final, meses_reales = calculate_mortgage(
        request.capital,
        request.interes_anual,
        request.plazo_anios,
        request.pagos_extra
    )
    return MortgageResponse(
        cuota_mensual=cuota,
        total_intereses=intereses,
        pago_total=total,
        amortizacion_anual=amortizacion,
        cuota_final=cuota_final,
        meses_reales=meses_reales
    )
