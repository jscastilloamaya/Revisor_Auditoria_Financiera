# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 12:15:51 2026

@author: Juan Castillo Amaya
"""
import pandas as pd

HOJAS_CONFIG=["RRHH", "Gastos de Operación", "Pers.Juridica", "Arriendo", "Servicios Básicos"]

def eliminar_columnas_sobrantes(df: pd.DataFrame, columna_final: str) -> pd.DataFrame:
    columna_base = columna_final
    df = df.iloc[:, :df.columns.get_loc(columna_base) + 1]
    return df

def pruebasbackbotones(variable: str):
    print(variable)