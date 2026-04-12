import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

client = TestClient(app)

def test_calcular_hipoteca_success():
    response = client.post(
        "/api/calcular",
        json={"capital": 200000, "interes_anual": 2.5, "plazo_anios": 20}
    )
    assert response.status_code == 200
    data = response.json()
    assert "cuota_mensual" in data
    assert "total_intereses" in data
    assert "pago_total" in data
    assert "amortizacion_anual" in data
    assert isinstance(data["amortizacion_anual"], list)
    assert len(data["amortizacion_anual"]) == 21

def test_calcular_hipoteca_invalid_capital():
    # Capital can't be negative or 0
    response = client.post(
        "/api/calcular",
        json={"capital": -1000, "interes_anual": 2.5, "plazo_anios": 20}
    )
    assert response.status_code == 422 # Unprocessable Entity

def test_calcular_hipoteca_missing_field():
    response = client.post(
        "/api/calcular",
        json={"capital": 100000, "plazo_anios": 20} # Missing interes_anual
    )
    assert response.status_code == 422
