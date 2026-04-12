import pytest
import sys
import os

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services import calculate_mortgage

def test_calculate_mortgage_standard():
    cuota, intereses, total, amortizacion = calculate_mortgage(capital=150000, interes_anual=3.5, plazo_anios=30)
    
    # Check basic bounds and values
    assert cuota == 673.57
    assert total > 150000
    assert intereses == round(total - 150000, 2)
    
    # 30 years means 31 entries (year 0 to year 30)
    assert len(amortizacion) == 31
    assert amortizacion[0]["year"] == 0
    assert amortizacion[0]["balance"] == 150000.0
    assert amortizacion[-1]["year"] == 30
    assert amortizacion[-1]["balance"] == 0.0

def test_calculate_mortgage_zero_interest():
    cuota, intereses, total, amortizacion = calculate_mortgage(capital=100000, interes_anual=0, plazo_anios=10)
    
    # Check 0% interest edge case
    assert cuota == round(100000 / (10 * 12), 2)
    assert intereses == 0.0
    assert total == 100000.0
    assert len(amortizacion) == 11
    assert amortizacion[-1]["balance"] == 0.0

