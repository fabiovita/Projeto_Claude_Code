"""
Calculadora do Sistema de Amortização Constante (SAC).
Amortização fixa, parcelas decrescentes.
"""
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd


def calcular_sac(
    valor: float,
    taxa_mensal: float,
    num_parcelas: int,
    primeira_parcela: date,
    carencia: int = 0,
    carencia_tipo: str = "capitalizado",
) -> pd.DataFrame:
    """
    Retorna DataFrame com as colunas:
    parcela, vencimento, saldo_inicial, juros, amortizacao, prestacao, saldo_final
    """
    rows = []
    saldo = valor
    amortizacao = None

    total_meses = carencia + num_parcelas
    for i in range(1, total_meses + 1):
        vencimento = primeira_parcela + relativedelta(months=i - 1)
        juros = saldo * taxa_mensal

        if i <= carencia:
            if carencia_tipo == "juros_pagos":
                # Paga apenas os juros; saldo não se altera
                prestacao = juros
                amort = 0.0
                saldo_final = saldo
            else:
                # Capitalizado: sem pagamento, juros incorporados ao saldo
                prestacao = 0.0
                amort = 0.0
                saldo_final = saldo + juros
        else:
            if amortizacao is None:
                amortizacao = saldo / num_parcelas
            amort = amortizacao
            prestacao = juros + amort
            saldo_final = max(saldo - amort, 0.0)

        rows.append({
            "parcela": i,
            "vencimento": vencimento,
            "saldo_inicial": round(saldo, 2),
            "juros": round(juros, 2),
            "amortizacao": round(amort, 2),
            "prestacao": round(prestacao, 2),
            "saldo_final": round(saldo_final, 2),
        })

        saldo = saldo_final

    return pd.DataFrame(rows)
