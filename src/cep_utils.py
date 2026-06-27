"""Funções auxiliares para Controle Estatístico do Processo (CEP)."""

from __future__ import annotations

import numpy as np
import pandas as pd


def imr_limits(values: pd.Series | np.ndarray) -> dict:
    """Calcula limites de gráfico I-MR para observações individuais.

    Usa o método clássico para subgrupos de tamanho 1:
    - sigma estimado por MRbar / d2, com d2 = 1,128 para amplitude móvel de 2 pontos;
    - limites do gráfico I: média ± 3*sigma;
    - limites do gráfico MR: CL = MRbar, UCL = 3,267*MRbar, LCL = 0.
    """
    series = pd.Series(values).dropna().astype(float)
    if len(series) < 3:
        raise ValueError("São necessárias pelo menos 3 observações para estimar limites I-MR.")

    x = series.to_numpy()
    mr = np.abs(np.diff(x))
    mrbar = float(np.mean(mr))
    d2 = 1.128
    d4 = 3.267
    sigma = mrbar / d2 if mrbar > 0 else 0.0
    center = float(np.mean(x))

    return {
        "center": center,
        "sigma": sigma,
        "ucl_i": center + 3 * sigma,
        "lcl_i": center - 3 * sigma,
        "mrbar": mrbar,
        "ucl_mr": d4 * mrbar,
        "lcl_mr": 0.0,
    }


def basic_spc_flags(values: pd.Series, limits: dict) -> pd.DataFrame:
    """Aplica regras básicas de alerta em série temporal.

    Regras implementadas:
    1) Ponto fora dos limites de controle.
    2) Nove pontos consecutivos acima ou abaixo da linha central.
    3) Seis pontos consecutivos crescentes ou decrescentes.
    """
    s = pd.Series(values).dropna().astype(float)
    cl = limits["center"]
    ucl = limits["ucl_i"]
    lcl = limits["lcl_i"]

    flags = pd.DataFrame(index=s.index)
    flags["valor"] = s
    flags["fora_limites"] = (s > ucl) | (s < lcl)

    side = np.where(s > cl, 1, np.where(s < cl, -1, 0))
    same_side_run = []
    run = 0
    last = 0
    for val in side:
        if val != 0 and val == last:
            run += 1
        elif val != 0:
            run = 1
            last = val
        else:
            run = 0
            last = 0
        same_side_run.append(run)
    flags["nove_mesmo_lado"] = np.array(same_side_run) >= 9

    diff = s.diff()
    trend_run = []
    run = 0
    last_sign = 0
    for d in diff.fillna(0):
        sign = 1 if d > 0 else (-1 if d < 0 else 0)
        if sign != 0 and sign == last_sign:
            run += 1
        elif sign != 0:
            run = 1
            last_sign = sign
        else:
            run = 0
            last_sign = 0
        trend_run.append(run)
    flags["seis_tendencia"] = np.array(trend_run) >= 5  # 6 pontos geram 5 diferenças na mesma direção
    flags["alerta"] = flags[["fora_limites", "nove_mesmo_lado", "seis_tendencia"]].any(axis=1)
    return flags
