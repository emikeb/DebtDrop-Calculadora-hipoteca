def calculate_mortgage(capital: float, interes_anual: float, plazo_anios: int, pagos_extra: list = None) -> tuple[float, float, float, list, float, int]:
    if pagos_extra is None:
        pagos_extra = []
    
    extras_por_mes = {}
    for p in pagos_extra:
        if p.mes not in extras_por_mes:
            extras_por_mes[p.mes] = []
        extras_por_mes[p.mes].append(p)

    interes_mensual = (interes_anual / 100) / 12 if interes_anual > 0 else 0
    meses_totales = plazo_anios * 12
    meses_restantes = meses_totales
    
    if interes_mensual > 0:
        cuota_mensual = capital * (interes_mensual * (1 + interes_mensual)**meses_restantes) / ((1 + interes_mensual)**meses_restantes - 1)
    else:
        cuota_mensual = capital / meses_restantes
        
    cuota_inicial = cuota_mensual
    cuota_regular = cuota_mensual
    balance_actual = capital
    amortizacion_anual = [{"year": 0, "balance": round(balance_actual, 2)}]
    
    total_pagado = 0
    
    mes = 1
    while balance_actual > 0.001 and mes <= meses_totales:
        interes_pago = balance_actual * interes_mensual
        capital_pago = cuota_regular - interes_pago
        
        cuota_pago = cuota_regular
        if capital_pago > balance_actual:
            capital_pago = balance_actual
            cuota_pago = capital_pago + interes_pago

        balance_actual -= capital_pago
        total_pagado += cuota_pago
        
        if balance_actual < 0:
            balance_actual = 0
            
        if mes in extras_por_mes:
            for extra in extras_por_mes[mes]:
                if extra.cantidad > balance_actual:
                    extra.cantidad = balance_actual
                
                balance_actual -= extra.cantidad
                total_pagado += extra.cantidad
                
                if extra.tipo.value == "cuota":
                    m_rest = meses_totales - mes
                    if m_rest > 0 and balance_actual > 0:
                        if interes_mensual > 0:
                            cuota_regular = balance_actual * (interes_mensual * (1 + interes_mensual)**m_rest) / ((1 + interes_mensual)**m_rest - 1)
                        else:
                            cuota_regular = balance_actual / m_rest

        if balance_actual < 0:
            balance_actual = 0

        if mes % 12 == 0:
            amortizacion_anual.append({"year": mes // 12, "balance": round(balance_actual, 2)})
        elif balance_actual == 0:
            year_finished_ceil = (mes + 11) // 12
            for y in range(year_finished_ceil, plazo_anios + 1):
                if not any(a["year"] == y for a in amortizacion_anual):
                    amortizacion_anual.append({"year": y, "balance": 0.0})
            break
            
        mes += 1

    if balance_actual <= 0.001:
        for y in range((mes // 12) + 1, plazo_anios + 1):
            if not any(a["year"] == y for a in amortizacion_anual):
                amortizacion_anual.append({"year": y, "balance": 0.0})

    total_intereses = total_pagado - capital
    meses_reales = mes if balance_actual <= 0.001 else mes - 1
    if meses_reales < 1:
        meses_reales = 1
    return round(cuota_inicial, 2), round(total_intereses, 2), round(total_pagado, 2), amortizacion_anual, round(cuota_regular, 2), meses_reales
