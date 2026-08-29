
"""
Created on Sat Jul 25 12:15:51 2026

@author: Juan Castillo Amaya
"""
import pandas as pd
import numpy as np
import re
from pandas.api.types import is_numeric_dtype
import math
import unicodedata
HOJAS_CONFIG=["RRHH", "Gastos de Operación", "Pers.Juridica", "Arriendo", "Servicios Básicos"]

# %% Variables de hojas
def variables_hoja(hoja: str)-> list:
    if hoja =="RRHH":
        colum_nombres= [
        "Glosa/Justificación",
        "RUT Contribuyente",
        "RUT RRHH",
        "Total Haberes Total Boleta",
        "Valor Rendido al Proyecto",
        "Fecha Emision Documento",
        "Fecha de Pago Real",
        "RRHH"]
    return colum_nombres

# %% Eliminar columnas sobrantes
def eliminar_columnas_sobrantes(df: pd.DataFrame, columna_final: str) -> pd.DataFrame:
    columna_base = columna_final
    df = df.iloc[:, :df.columns.get_loc(columna_base) + 1]
    return df
# %% Funciones de limpieza para eliminar filas vacias y las que dicen Total
def convertir_a_numerico(df: pd.DataFrame, columna: str) -> pd.DataFrame:
    """
    Convierte la columna indicada a valores numéricos.
    Texto, vacíos o valores inválidos se convierten en NaN.
    """
    df = df.copy()
    df[columna] = pd.to_numeric(df[columna], errors="coerce")
    return df


def filtrar_mayores_igual(df: pd.DataFrame, columna: str, minimo: float) -> pd.DataFrame:
    """
    Conserva únicamente filas donde la columna >= minimo.
    Los valores NaN también se eliminan automáticamente.
    """
    df = df.copy()
    return df[df[columna] >= minimo]




def eliminar_filas_con_valor_en_columna(df: pd.DataFrame, columna: str, valor: str = "Total") -> pd.DataFrame:
    """
    Elimina las filas donde la columna indicada contiene exactamente el valor especificado.
    - df: DataFrame de entrada
    - columna: nombre de la columna a verificar
    - valor: valor que, si aparece, causa la eliminación de esa fila
    """
    df = df.copy()
    return df[df[columna] != valor]



def limpiar_por_columna(df: pd.DataFrame, columna: str, minimo: float = 1) -> pd.DataFrame:
    """
    Limpieza completa basada en una columna específica:
    - convierte la columna a numérico
    - elimina texto, vacíos y NaN
    - conserva solo valores >= minimo
    """
    df = convertir_a_numerico(df, columna)
    df = filtrar_mayores_igual(df, columna, minimo)
    df = eliminar_filas_con_valor_en_columna(df, columna="Cuenta", valor="Total")
    return df



# %% Funcion para verificar si no se rinde nada (Dataframe vacio)
def dataframe_solo_con_cabeceras(df: pd.DataFrame) -> bool:
    """
    Retorna True si el DataFrame no contiene filas de datos,
    es decir, si únicamente tiene las cabeceras.
    """
    return df.shape[0] == 0
# %%  Funcion para los formatos de los RUT   
#Funcion para los formatos de los RUT
def columna_normalizar_alnum(df, col, *, 
                             nombre_salida=None,
                             sep_miles=None, 
                             coma_decimal=False,
                             strip=True,
                             colapsar_decimales=True):
    """
    Procesa df[col] y devuelve df con esa columna en texto (StringDtype),
    cumpliendo: sin puntos ni caracteres especiales; solo números y letras.

    Reglas:
      1) Si el valor es numérico y es un flotante entero (p. ej., 15.0, "0015.00"):
         -> "15" (texto, solo dígitos).
      2) Si el valor es numérico con decimales reales (p. ej., 12.5):
         -> si colapsar_decimales=True: quitar el separador decimal (p. ej., "125");
            si False: conservar forma textual (normalizada), pero luego limpiar a alfanumérico (quitar punto/coma).
      3) Si el valor NO es numérico: se limpia a solo caracteres alfanuméricos (A-Za-z0-9).

    Parámetros:
      - nombre_salida: si se indica, escribe en esa columna; si no, sobrescribe `col`.
      - sep_miles: carácter separador de miles a eliminar primero (p. ej., ',', '.', ' ').
      - coma_decimal: si True, interpreta coma como separador decimal (ej.: "12,5" -> 12.5).
      - strip: recorta espacios en strings antes de procesar.
      - colapsar_decimales: True (por defecto) elimina el separador decimal en decimales reales.
                            False los deja textual (pero sin el separador al final por la limpieza alfanumérica).

    Retorna:
      - df: el mismo DataFrame, con la columna transformada a StringDtype.
    """
    destino = nombre_salida or col
    s = df[col].astype("string")

    # 1) Preparación de texto
    if strip:
        s = s.str.strip()

    # 2) Normalización opcional de formato numérico (miles/decimal)
    #    * Primero eliminamos sep_miles si se especifica.
    if sep_miles:
        s_norm = s.str.replace(sep_miles, "", regex=False)
    else:
        s_norm = s

    #    * Si coma_decimal=True, convertimos coma decimal a punto para poder parsear
    if coma_decimal:
        s_norm = s_norm.str.replace(",", ".", regex=False)

    # 3) Intento de parseo numérico
    num = pd.to_numeric(s_norm, errors="coerce")
    es_num = num.notna() & np.isfinite(num)
    es_entero_exacto = es_num & (num == np.floor(num))

    # 4) Construcción de salida como texto
    out = s.copy()

    # 4a) Flotante entero -> "entero" (sin separadores, solo dígitos)
    out.loc[es_entero_exacto] = num.loc[es_entero_exacto].astype("Int64").astype("string")

    # 4b) Numérico con decimales reales
    es_decimal_real = es_num & ~es_entero_exacto
    if es_decimal_real.any():
        if colapsar_decimales:
            # Quitamos el separador decimal unificando a texto "sin punto"
            # Ej.: 12.5 -> "125", 100.05 -> "10005"
            txt = s_norm.loc[es_decimal_real].astype("string")
            # A esta altura el decimal es con punto si coma_decimal=True se normalizó
            txt = txt.str.replace(".", "", regex=False)
            out.loc[es_decimal_real] = txt
        else:
            # Mantenemos representación textual normalizada (con '.' si correspondía),
            # luego al final limpiaremos caracteres no alfanuméricos (lo cual quitará el '.')
            out.loc[es_decimal_real] = s_norm.loc[es_decimal_real].astype("string")

    # 4c) No numéricos: se dejan para limpieza final

    # 5) Limpieza final: dejar solo alfanuméricos (A-Za-z0-9), quitar todo lo demás
    #    Si la celda es NA, se mantiene como <NA>.
    def solo_alnum(val: str):
        if val is None or pd.isna(val):
            return pd.NA
        # Eliminar todo lo que no sea [A-Za-z0-9]
        limpio = re.sub(r'[^A-Za-z0-9]', '', val)
        # Si termina vacío, lo dejamos como <NA> para no introducir cadenas vacías
        return limpio if limpio != "" else pd.NA

    out = out.map(solo_alnum)

    df[destino] = out.astype("string")
    return df

# %% Limpiar puntos flotantes en las columnas

def limpiar_decimales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina (trunca) la parte decimal en todo el DataFrame:
      - En columnas numéricas: devuelve enteros (pandas 'Int64' con soporte de NA).
      - En columnas no numéricas: convierte textos numéricos (p. ej. '3.14') a su parte entera como texto ('3').
      - No redondea: solo truncado hacia 0 (np.trunc).
    """
    df = df.copy()

    # 1) Columnas numéricas -> enteros (Int64), truncado
    for col in df.columns:
        if is_numeric_dtype(df[col]):
            s = pd.to_numeric(df[col], errors="coerce")
            out = np.trunc(s)  # truncado hacia 0
            out = pd.Series(out, index=s.index).replace([np.inf, -np.inf], np.nan)
            df[col] = out.astype("Int64")
    
    # 2) Columnas no numéricas -> transformar solo celdas que sean números en texto
    def trunc_str_num(x):
        # Dejar None/NaN tal cual
        if x is None or (isinstance(x, float) and np.isnan(x)):
            return x
        # Intentar parsear a número desde string u otros tipos
        try:
            # Permitir strings con espacios o comas decimales comunes
            if isinstance(x, str):
                s = x.strip().replace(",", ".")
            else:
                s = str(x)
            val = float(s)
        except Exception:
            return x  # no parece número -> dejar igual
        # Truncar hacia 0 y devolver como string sin decimales
        if np.isinf(val) or np.isnan(val):
            return x  # conservar representaciones especiales
        return str(int(np.trunc(val)))

    for col in df.columns:
        if not is_numeric_dtype(df[col]):
            df[col] = df[col].apply(trunc_str_num)

    return df


# %% Eliminar los espacio en la glosa
def limpiar_saltos_linea(df, columna):
    # Reemplaza saltos de línea (\n y \r) por un espacio o vacío
    df[columna] = df[columna].astype(str).str.replace(r'[\r\n]+', ' ', regex=True)
    return df

# %% Funcion de procesado de la hoja 
# Unicamente verifica que la hoja existe y no se encuentra vacia
 
def procesar_hoja(df: pd.DataFrame, RUT1: str, RUT2: str, columna_final: str) -> pd.DataFrame:
    "Llama a todas las funciones para procesar la hoja"
    df = eliminar_columnas_sobrantes(df,columna_final) 
    df = limpiar_por_columna(df, columna="Valor Rendido al Proyecto", minimo=1) # Filas vacias o sin rendir
    df = columna_normalizar_alnum(df, RUT1) # Formato a los rut
    df = columna_normalizar_alnum(df, RUT2) # Formato a los rut
    df = limpiar_decimales(df)
    df = limpiar_saltos_linea(df, columna_final)
    if dataframe_solo_con_cabeceras(df):
        print("La Hoja no tiene nada por rendir")
        Tiene_Datos = False
    else:
        print("La Hoja tiene valores por rendir")
        Tiene_Datos = True
    return df, Tiene_Datos    


# %% Verificador de longitud de RUT 
_ZW_RE = re.compile(r"[\u200B-\u200D\uFEFF\u00A0]")

def _normalizar_str(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = _ZW_RE.sub("", s)
    s = s.strip()
    return s

def imprimir_filas_invalidas_alnum9(df: pd.DataFrame, columna: str, columnas_tabla: list, incluir_nan: bool = True) -> pd.DataFrame:
    """
    Verifica que los valores de `columna` sean exactamente 9 caracteres alfanuméricos.
    Retorna un DataFrame con las filas inválidas (incluyendo NaN/None si incluir_nan=True),
    listo para que el frontend lo muestre en una ventana.
    """
    if columna not in df.columns:
        raise KeyError(f"La columna '{columna}' no existe en el DataFrame.")

    for c in columnas_tabla:
        if c not in df.columns:
            raise KeyError(f"La columna '{c}' no existe en el DataFrame.")

    patron = re.compile(r"^[A-Za-z0-9]{9}$")
    filas_invalidas = []

    for idx, row in df.iterrows():
        val = row[columna]

        if val is None or pd.isna(val):
            if incluir_nan:
                fila_dict = row[columnas_tabla].to_dict()
                fila_dict["Longitud"] = 0
                filas_invalidas.append(fila_dict)
            continue

        s = _normalizar_str(str(val))
        if not patron.fullmatch(s):
            fila_dict = row[columnas_tabla].to_dict()
            fila_dict["Longitud"] = len(s)
            filas_invalidas.append(fila_dict)

    tabla = pd.DataFrame(filas_invalidas)
    return tabla    

# %% Modulo de Auditoria de columnas 

def auditar_hoja(df: pd.DataFrame, Rut1: str, Rut2: str, Monto1: str, Monto2: str, FechaEmitido: str, FechaPagado: str, Hoja: str  ) -> pd.DataFrame:
    "Llama a las funciones de verificación"
    resultados = []
    
    Errores_RUT1 = imprimir_filas_invalidas_alnum9(df, Rut1, columnas_tabla=[Rut1])
    resultados.append((Rut1, Errores_RUT1))
    
    Errores_RUT2 = imprimir_filas_invalidas_alnum9(df, Rut2, columnas_tabla=[Rut2])
    resultados.append((Rut2, Errores_RUT2))
    
    return resultados