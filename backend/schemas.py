from pydantic import BaseModel, Field
from typing import List

class MortgageRequest(BaseModel):
    capital: float = Field(..., gt=0, description="Capital inicial del préstamo")
    interes_anual: float = Field(..., ge=0, description="Tasa de interés anual en % (ej. 3.5)")
    plazo_anios: int = Field(..., gt=0, description="Plazo de amortización en años")

class AmortizationYear(BaseModel):
    year: int
    balance: float

class MortgageResponse(BaseModel):
    cuota_mensual: float
    total_intereses: float
    pago_total: float
    amortizacion_anual: List[AmortizationYear]
