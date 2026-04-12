def calculate_mortgage(capital: float, interes_anual: float, plazo_anios: int) -> tuple[float, float, float, list]:
    if interes_anual == 0:
        cuota_mensual = capital / (plazo_anios * 12)
        interes_mensual = 0
    else:
        interes_mensual = (interes_anual / 100) / 12
        numero_pagos = plazo_anios * 12
        cuota_mensual = capital * (interes_mensual * (1 + interes_mensual)**numero_pagos) / ((1 + interes_mensual)**numero_pagos - 1)
    
    pago_total = cuota_mensual * (plazo_anios * 12)
    total_intereses = pago_total - capital
    
    amortizacion_anual = []
    balance_actual = capital
    amortizacion_anual.append({"year": 0, "balance": round(balance_actual, 2)})
    
    for anio in range(1, plazo_anios + 1):
        for _ in range(12):
            interes_pago = balance_actual * interes_mensual
            capital_pago = cuota_mensual - interes_pago
            balance_actual -= capital_pago
            if balance_actual < 0:
                balance_actual = 0
                
        amortizacion_anual.append({"year": anio, "balance": round(balance_actual, 2)})
    
    return round(cuota_mensual, 2), round(total_intereses, 2), round(pago_total, 2), amortizacion_anual
