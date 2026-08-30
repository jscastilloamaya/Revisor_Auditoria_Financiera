# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 12:18:14 2026

@author: Juan Castillo Amaya
"""
from tkinter.filedialog import askopenfilename
from tkinter import Tk, messagebox, Button
from tkinter import Toplevel, Text, Scrollbar, END
import sys
import backendauditor as bka
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")#Ignorar los warnigs del lector
# %% Lectura del archivo
def seleccionar_archivo_excel()-> str:
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
# %% Ventana para procesar las hojas
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
            f"La hoja '{nombre_hoja}' no existe en el archivo.\n\n"
            "Se omitirá esta sección del programa."
        )
        return None, False


    except FileNotFoundError:
        messagebox.showwarning(
        "Archivo no encontrada",
        f"❌El archivo '{ArchivoNombre}' no encontrado, es posible que se moviera de su ubicación original."
    )
        raise SystemExit(f"❌ El archivo '{ArchivoNombre}' no se encontró. Programa detenido.")

    except Exception as e:
        messagebox.showerror(
        "Error al leer el Excel",
        f"Ocurrió un error al leer el Excel: {e}\n\n"
        "Es posible que tenga el archivo abierto mientras se intenta leer, ciérrelo para poder leerlo."
        )
    raise SystemExit("❌ Ocurrió un error al leer el Excel.")


###Ventana de Auditoria  


def exportar_csv(df, nombre_hoja, archivo_origen):
    try:
        ruta_csv = bka.convertir_csv(df, nombre_hoja, archivo_origen)
        messagebox.showinfo("Exportación exitosa", f"Archivo guardado en:\n{ruta_csv}")
    except Exception as e:
        messagebox.showerror("Error al exportar", f"No se pudo generar el CSV:\n{e}")


def abrir_ventana_resultados(ventana_padre, titulo_hoja, df, archivo_origen):
    top = Toplevel(ventana_padre)
    top.title(f"Resultados - {titulo_hoja}")
    top.geometry("700x550")

    boton_exportar = Button(top, text="Exportar a CSV",
                             command=lambda: exportar_csv(df, titulo_hoja, archivo_origen))
    boton_exportar.pack(pady=5)

    scrollbar = Scrollbar(top)
    scrollbar.pack(side="right", fill="y")

    texto = Text(top, wrap="word", yscrollcommand=scrollbar.set)
    texto.pack(expand=True, fill="both")
    scrollbar.config(command=texto.yview)

    texto.tag_config("ok", foreground="green")
    texto.tag_config("warn", foreground="#b8860b")

    return texto

def agregar_resultado_tabla(texto_widget, tabla, titulo):
    """Inserta el resultado de una validación (tabla del backend) en el Text."""
    if tabla.empty:
        texto_widget.insert(END, f"✅ Todo correcto: '{titulo}'\n\n", "ok")
    else:
        texto_widget.insert(END, f"⚠️ Por favor revisar: {titulo}\n", "warn")
        texto_widget.insert(END, tabla.to_string(index=False) + "\n\n")



def procesar_cuenta (ArchivoNombre, nombre_hoja):
    hoja, habilitador =cargar_hoja_excel(ArchivoNombre, nombre_hoja)
    if habilitador == True:
        columnas_nombres=bka.variables_hoja(nombre_hoja)
        dfcuenta,ConDatos = bka.procesar_hoja(hoja, columnas_nombres[1], columnas_nombres[2], columnas_nombres[0])
        print("Leido con exito"+ columnas_nombres[0])
        if ConDatos == False:
            messagebox.showwarning(
            "Hoja sin datos",
            f"La hoja '{nombre_hoja}' se encuentra vacía."
            )
        elif ConDatos == True:
            resultados_auditoria = bka.auditar_hoja(dfcuenta, columnas_nombres[1], columnas_nombres[2], columnas_nombres[3], columnas_nombres[4],  columnas_nombres[5],  columnas_nombres[6], nombre_hoja)
            texto_widget = abrir_ventana_resultados(ventana, nombre_hoja, dfcuenta, ArchivoNombre)
            for titulo, tabla in resultados_auditoria:
                agregar_resultado_tabla(texto_widget, tabla, titulo)
    return



# %% Ventana principal

ventana = Tk()
ventana.title("Programa Auditor")
ventana.geometry("400x280")

boton_rrhh = Button(ventana, text="Recursos Humanos", command=lambda:  procesar_cuenta (ArchivoNombre, nombres_hojas[0]))
boton_rrhh.pack(pady=5)

boton_gastos = Button(ventana, text="Gastos de Operación", command=lambda: procesar_cuenta (ArchivoNombre, nombres_hojas[1]))
boton_gastos.pack(pady=5)

boton_gastos = Button(ventana, text="Personas Jirídicas", command=lambda: procesar_cuenta (ArchivoNombre, nombres_hojas[2]))
boton_gastos.pack(pady=5)

boton_gastos = Button(ventana, text="Arriendos", command=lambda: procesar_cuenta (ArchivoNombre, nombres_hojas[3]))
boton_gastos.pack(pady=5)

boton_gastos = Button(ventana, text="Servicios Básicos", command=lambda: procesar_cuenta (ArchivoNombre, nombres_hojas[4]))
boton_gastos.pack(pady=5)
# ... y así para  Arriendo, Servicios Básicos

ventana.mainloop()

    
    