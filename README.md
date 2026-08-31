# Auditor de Fiscalizaciones — Cargas SGP Corfo

Herramienta para auditar automáticamente los archivos Excel de rendición utilizados en Corfo, revisando de forma consistente las hojas **RRHH**, **Gastos de Operación**, **Pers. Jurídica**, **Arriendo** y **Servicios Básicos**.

El proyecto tiene dos versiones, pensadas para distintos tipos de usuario:

1. **Notebook** (`AuditorFisc_V2.ipynb`) — para uso técnico, análisis exploratorio o modificaciones rápidas.
2. **Aplicación de escritorio** (interfaz gráfica en `tkinter`, empaquetada como `.exe`) — para uso de colegas no técnicos, sin necesidad de tener Python instalado.

---

## 📁 Estructura del proyecto

```
.
├── AuditorFisc_V2.ipynb      # Notebook original (versión exploratoria)
├── backendauditor/           # Lógica de auditoría (backend puro, sin UI)
├── frontendauditor.py        # Interfaz gráfica (tkinter)
├── dist/                     # Ejecutable generado (.exe) — no versionado
└── README.md
```

La lógica de negocio vive únicamente en `backendauditor/`; el frontend solo se encarga de mostrar los resultados que el backend le entrega.

---

## 🚀 Uso

### Opción 1: Notebook
Pensado para uso técnico o exploración de datos.

```bash
conda activate auditor-fiscal
jupyter notebook AuditorFisc_V2.ipynb
```

### Opción 2: Aplicación de escritorio (recomendada para uso general)
No requiere Python instalado. Basta con ejecutar el `.exe` generado y cargar el archivo Excel de rendición a auditar.

---

## 🛠️ Requisitos (para desarrollo)

- Python 3.11 (via miniforge/conda)
- Entorno `auditor-fiscal` con:
  - `pandas`
  - `numpy`
  - `openpyxl`

```bash
conda create -n auditor-fiscal python=3.11
conda activate auditor-fiscal
pip install pandas numpy openpyxl pyinstaller
```

---

## 📦 Generar el ejecutable

```bash
pyinstaller --onefile --windowed frontendauditor.py
```

El `.exe` resultante queda en `dist/` y funciona en máquinas sin Python instalado.

---

## 📝 Notas

- Este README cubre ambas versiones del proyecto (notebook y GUI) como parte de un mismo historial de desarrollo.
- Pendiente: unificar `cargar_hoja_excel()`, actualmente duplicada entre frontend y backend.
