# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 12:18:14 2026

@author: Juan Castillo Amaya
"""
from tkinter.filedialog import askopenfilename
from tkinter import Tk, messagebox, Button
import sys
import backendauditor as bka


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

ArchivoNombre = seleccionar_archivo_excel()

###########
######### Ventana principal
############
nombres_hojas = list(bka.HOJAS_CONFIG)


def al_hacer_clic_hoja(hoja):
    print(f"Hoja seleccionada: {hoja}")  #  para probar botones


ventana = Tk()
ventana.title("Programa Auditor")
ventana.geometry("400x280")
boton_rrhh = Button(ventana, text="RRHH", command=lambda: al_hacer_clic_hoja("RRHH"))
boton_rrhh.pack(pady=5)

boton_gastos = Button(ventana, text="Gastos de Operación", command=lambda: al_hacer_clic_hoja("Gastos de Operación"))
boton_gastos.pack(pady=5)

# ... y así para Pers.Juridica, Arriendo, Servicios Básicos

ventana.mainloop()

