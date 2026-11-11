# Dashboard de Ventas

Dashboard interactivo construido con **Streamlit** para explorar datos de ventas por tienda y por estado.

## Estructura del repositorio

```
.
├── app.py                # Aplicación Streamlit (punto de entrada)
├── parte_1sample.csv     # Datos de ventas (muestra, parte 1)
└── parte_2sample.csv     # Datos de ventas (muestra, parte 2)
```

## Requisitos

```bash
pip install streamlit pandas
```

## Ejecución

```bash
streamlit run app.py
```

La aplicación abre 4 pestañas: **Visión Global**, **Por tienda**, **Por estado** y **Sorpresa**.

## Nota

Este repositorio ya está vinculado a un remoto existente en GitHub (`TeresaSangil/ProyectoVisualizacion`). Si vas a actualizarlo, usa el flujo normal:

```bash
git add .
git commit -m "mensaje del cambio"
git push origin main
```

en vez de crear un repositorio nuevo.
