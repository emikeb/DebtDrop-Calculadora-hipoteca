import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services import MortgageCalculator
from schemas import AmortizacionAnticipada, TipoAmortizacion, MortgageRequest

def test_calculate_mortgage_standard():
    req = MortgageRequest(capital=150000, interes_anual=3.5, plazo_anios=30)
    resp = MortgageCalculator(req).calculate()
    
    # Use approx due to float iteration drift
    assert resp.cuota_mensual == pytest.approx(673.57, abs=0.1)
    assert resp.pago_total > 150000
    assert resp.total_intereses == pytest.approx(resp.pago_total - 150000, abs=0.1)
    
    assert len(resp.amortizacion_anual) == 31
    assert resp.amortizacion_anual[0].year == 0
    assert resp.amortizacion_anual[0].balance == pytest.approx(150000.0, abs=0.1)
    assert resp.amortizacion_anual[-1].year == 30
    assert resp.amortizacion_anual[-1].balance == pytest.approx(0.0, abs=1.0)

def test_calculate_mortgage_zero_interest():
    req = MortgageRequest(capital=100000, interes_anual=0, plazo_anios=10)
    resp = MortgageCalculator(req).calculate()
    
    assert resp.cuota_mensual == pytest.approx(100000 / (10 * 12), abs=0.1)
    assert resp.total_intereses == 0.0
    assert resp.pago_total == pytest.approx(100000.0, abs=0.1)
    assert len(resp.amortizacion_anual) == 11
    assert resp.amortizacion_anual[-1].balance == pytest.approx(0.0, abs=1.0)

def test_amortizacion_reduce_plazo():
    ext = AmortizacionAnticipada(mes=12, cantidad=10000, tipo=TipoAmortizacion.plazo)
    req = MortgageRequest(capital=150000, interes_anual=3.5, plazo_anios=30, pagos_extra=[ext])
    resp = MortgageCalculator(req).calculate()
    
    assert resp.cuota_mensual == pytest.approx(673.57, abs=0.1)
    # Total expected is around 226,417
    assert resp.pago_total == pytest.approx(226417.1, abs=5.0)
    assert resp.pago_total < 242400
    
def test_amortizacion_reduce_cuota():
    ext = AmortizacionAnticipada(mes=12, cantidad=10000, tipo=TipoAmortizacion.cuota)
    req = MortgageRequest(capital=150000, interes_anual=3.5, plazo_anios=30, pagos_extra=[ext])
    resp = MortgageCalculator(req).calculate()
    
    # Initial cuota stays the same in the return signature
    assert resp.cuota_mensual == pytest.approx(673.57, abs=0.1)
    assert len(resp.amortizacion_anual) == 31
    assert resp.pago_total < 242400
