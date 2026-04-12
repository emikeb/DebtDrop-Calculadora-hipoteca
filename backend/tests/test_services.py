import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services import calculate_mortgage
from schemas import AmortizacionAnticipada, TipoAmortizacion

def test_calculate_mortgage_standard():
    cuota, intereses, total, amortizacion = calculate_mortgage(capital=150000, interes_anual=3.5, plazo_anios=30)
    
    # Use approx due to float iteration drift
    assert cuota == pytest.approx(673.57, abs=0.1)
    assert total > 150000
    assert intereses == pytest.approx(total - 150000, abs=0.1)
    
    assert len(amortizacion) == 31
    assert amortizacion[0]["year"] == 0
    assert amortizacion[0]["balance"] == pytest.approx(150000.0, abs=0.1)
    assert amortizacion[-1]["year"] == 30
    assert amortizacion[-1]["balance"] == pytest.approx(0.0, abs=1.0)

def test_calculate_mortgage_zero_interest():
    cuota, intereses, total, amortizacion = calculate_mortgage(capital=100000, interes_anual=0, plazo_anios=10)
    
    assert cuota == pytest.approx(100000 / (10 * 12), abs=0.1)
    assert intereses == 0.0
    assert total == pytest.approx(100000.0, abs=0.1)
    assert len(amortizacion) == 11
    assert amortizacion[-1]["balance"] == pytest.approx(0.0, abs=1.0)

def test_amortizacion_reduce_plazo():
    ext = AmortizacionAnticipada(mes=12, cantidad=10000, tipo=TipoAmortizacion.plazo)
    cuota, intereses, total, amortizacion = calculate_mortgage(capital=150000, interes_anual=3.5, plazo_anios=30, pagos_extra=[ext])
    
    assert cuota == pytest.approx(673.57, abs=0.1)
    # Total expected is around 226,417
    assert total == pytest.approx(226417.1, abs=5.0)
    assert total < 242400
    
def test_amortizacion_reduce_cuota():
    ext = AmortizacionAnticipada(mes=12, cantidad=10000, tipo=TipoAmortizacion.cuota)
    cuota, intereses, total, amortizacion = calculate_mortgage(capital=150000, interes_anual=3.5, plazo_anios=30, pagos_extra=[ext])
    
    # Initial cuota stays the same in the return signature
    assert cuota == pytest.approx(673.57, abs=0.1)
    assert len(amortizacion) == 31
    assert total < 242400

