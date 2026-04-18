from schemas import MortgageRequest, MortgageResponse

class MortgageCalculator:
    """Clase para simular y calcular la amortización de una hipoteca."""
    
    def __init__(self, request: MortgageRequest):
        self.request = request
        self.capital = request.capital
        self.interes_anual = request.interes_anual
        self.plazo_anios = request.plazo_anios
        self.pagos_extra = request.pagos_extra or []
        
        # Inicialización de estado
        self.interes_mensual = (self.interes_anual / 100) / 12 if self.interes_anual > 0 else 0
        self.meses_totales = self.plazo_anios * 12
        
        if self.interes_mensual > 0:
            self.cuota_mensual = self.capital * (self.interes_mensual * (1 + self.interes_mensual)**self.meses_totales) / ((1 + self.interes_mensual)**self.meses_totales - 1)
        else:
            self.cuota_mensual = self.capital / self.meses_totales
            
        self.cuota_inicial = self.cuota_mensual
        self.cuota_regular = self.cuota_mensual
        self.balance_actual = self.capital
        self.total_pagado = 0.0
        self.amortizacion_anual = [{"year": 0, "balance": round(self.balance_actual, 2)}]
        
        self.extras_por_mes = {}
        for p in self.pagos_extra:
            self.extras_por_mes.setdefault(p.mes, []).append(p)

    def calculate(self) -> MortgageResponse:
        mes = 1
        while self.balance_actual > 0.001 and mes <= self.meses_totales:
            self._process_month(mes)
            mes += 1

        self._finalize_amortization(mes)
        
        total_intereses = self.total_pagado - self.capital
        meses_reales = mes if self.balance_actual <= 0.001 else mes - 1
        if meses_reales < 1:
            meses_reales = 1
            
        return MortgageResponse(
            cuota_mensual=round(self.cuota_inicial, 2),
            total_intereses=round(total_intereses, 2),
            pago_total=round(self.total_pagado, 2),
            amortizacion_anual=self.amortizacion_anual,
            cuota_final=round(self.cuota_regular, 2),
            meses_reales=meses_reales
        )

    def _process_month(self, mes: int):
        interes_pago = self.balance_actual * self.interes_mensual
        capital_pago = self.cuota_regular - interes_pago
        
        cuota_pago = self.cuota_regular
        if capital_pago > self.balance_actual:
            capital_pago = self.balance_actual
            cuota_pago = capital_pago + interes_pago

        self.balance_actual -= capital_pago
        self.total_pagado += cuota_pago
        
        if self.balance_actual < 0:
            self.balance_actual = 0
            
        if mes in self.extras_por_mes:
            self._apply_extra_payments(mes)

        if self.balance_actual < 0:
            self.balance_actual = 0

        self._record_amortization(mes)

    def _apply_extra_payments(self, mes: int):
        for extra in self.extras_por_mes[mes]:
            if extra.cantidad > self.balance_actual:
                extra.cantidad = self.balance_actual
            
            self.balance_actual -= extra.cantidad
            self.total_pagado += extra.cantidad
            
            if extra.tipo.value == "cuota":
                m_rest = self.meses_totales - mes
                if m_rest > 0 and self.balance_actual > 0:
                    if self.interes_mensual > 0:
                        self.cuota_regular = self.balance_actual * (self.interes_mensual * (1 + self.interes_mensual)**m_rest) / ((1 + self.interes_mensual)**m_rest - 1)
                    else:
                        self.cuota_regular = self.balance_actual / m_rest

    def _record_amortization(self, mes: int):
        if mes % 12 == 0:
            self.amortizacion_anual.append({"year": mes // 12, "balance": round(self.balance_actual, 2)})
        elif self.balance_actual == 0:
            year_finished_ceil = (mes + 11) // 12
            for y in range(year_finished_ceil, self.plazo_anios + 1):
                if not any(a["year"] == y for a in self.amortizacion_anual):
                    self.amortizacion_anual.append({"year": y, "balance": 0.0})

    def _finalize_amortization(self, mes: int):
        if self.balance_actual <= 0.001:
            for y in range((mes // 12) + 1, self.plazo_anios + 1):
                if not any(a["year"] == y for a in self.amortizacion_anual):
                    self.amortizacion_anual.append({"year": y, "balance": 0.0})
