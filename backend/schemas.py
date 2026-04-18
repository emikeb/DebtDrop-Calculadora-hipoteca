from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class TipoAmortizacion(str, Enum):
    cuota = "cuota"
    plazo = "plazo"

class AmortizacionAnticipada(BaseModel):
    mes: int = Field(..., gt=0, description="Mes en el que se hace el pago")
    cantidad: float = Field(..., gt=0, description="Cantidad aportada")
    tipo: TipoAmortizacion = Field(..., description="Reducir cuota o plazo")

class MortgageRequest(BaseModel):
    capital: float = Field(..., gt=0, description="Capital inicial del préstamo")
    interes_anual: float = Field(..., ge=0, description="Tasa de interés anual en % (ej. 3.5)")
    plazo_anios: int = Field(..., gt=0, description="Plazo de amortización en años")
    pagos_extra: Optional[List[AmortizacionAnticipada]] = Field(default_factory=list)

class AmortizationYear(BaseModel):
    year: int
    balance: float

class MortgageResponse(BaseModel):
    cuota_mensual: float
    total_intereses: float
    pago_total: float
    amortizacion_anual: List[AmortizationYear]
    cuota_final: Optional[float] = None
    meses_reales: Optional[int] = None

