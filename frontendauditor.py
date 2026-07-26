# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 12:18:14 2026

@author: Juan Castillo Amaya
"""
from tkinter.filedialog import askopenfilename
from tkinter import Tk, messagebox, Button
import sys
import backendauditor as bka
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")#Ignorar los warnigs del lector
############
###### Lectura del archivo
############
def seleccionar_archivo_excel():
    while True:    
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        root.update()

        ArchivoNombre = askopenfilename(
            title="Selecciona un archivo de Excel",
            filetypes=[("Archivos de Excel", "*.xlsx *.xls")],
            parent=root
        )
    
        root.destroy()
        if ArchivoNombre:
            return ArchivoNombre

        reintentar = messagebox.askretrycancel(
            "Sin archivo seleccionado",
            "No seleccionaste ningún archivo. ¿Quieres intentar de nuevo?"
        )

        if not reintentar:
            sys.exit("❌ Programa detenido por el usuario.")

###########
######### Ventana principal
############
ArchivoNombre = seleccionar_archivo_excel()
nombres_hojas = list(bka.HOJAS_CONFIG)


def al_hacer_clic_hoja(hoja):
    print(f"Hoja seleccionada: {hoja}")  #  para probar botones



def cargar_hoja_excel(ArchivoNombre, nombre_hoja):
    try:
        df = pd.read_excel(ArchivoNombre, sheet_name=nombre_hoja, engine='openpyxl')
        return df, True

    except ValueError:
        messagebox.showwarning(
        "Hoja no encontrada",
        f"La hoja '{nombre_hoja}' no existe en el archivo. Se omitirán módulos dependientes."
    )
        print(f"La hoja '{nombre_hoja}' no existe en el archivo. Se omitirán módulos dependientes.")
        return None, False

    except FileNotFoundError:
        messagebox.showwarning(
        "Archivo no encontrada",
        f"El archivo '{ArchivoNombre}' no encontrado, es posible que se moviera de su ubicación original."
    )
        raise SystemExit(f"❌ El archivo '{ArchivoNombre}' no se encontró. Programa detenido.")

    except Exception as e:
        messagebox.showerror(
        "Error al leer el Excel",
        f"Ocurrió un error al leer el Excel: {e}\n\n"
        "Es posible que tenga el archivo abierto mientras se intenta leer, ciérrelo para poder leerlo."
        )
    raise SystemExit("❌ Ocurrió un error al leer el Excel.")

def procesar_cuenta (ArchivoNombre, nombre_hoja):
    hoja, habilitador =cargar_hoja_excel(ArchivoNombre, nombre_hoja)
    if habilitador == True:
        print("Leido con exito")
        
        
    return hoja





ventana = Tk()
ventana.title("Programa Auditor")
ventana.geometry("400x280")
boton_rrhh = Button(ventana, text="Recursos Humanos", command=lambda:  procesar_cuenta (ArchivoNombre, nombres_hojas[0]))
boton_rrhh.pack(pady=5)

boton_gastos = Button(ventana, text="Gastos de Operación", command=lambda: al_hacer_clic_hoja("Gastos de Operación"))
boton_gastos.pack(pady=5)

# ... y así para Pers.Juridica, Arriendo, Servicios Básicos

ventana.mainloop()

    
    