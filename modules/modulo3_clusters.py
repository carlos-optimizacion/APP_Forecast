import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.express as px

def mostrar():
    st.title("📊 Módulo 3: Clusterización Estratégica")

    carpeta_data = "Data"
    if not os.path.exists(carpeta_data):
        st.warning("📂 No hay carpeta /Data.")
        return

    archivos = [f for f in os.listdir(carpeta_data) if f.endswith((".xlsx", ".xls"))]
    if not archivos:
        st.warning("📁 No hay archivos Excel disponibles en /Data.")
        return

    archivo = st.selectbox("Selecciona un archivo:", archivos)
    df = pd.read_excel(os.path.join(carpeta_data, archivo))

    columnas_requeridas = [
        "Fecha", "Nombre_Producto", "Ventas_Unidades", 
        "Precio_Compra", "Precio_Venta", "ID_Cliente", "Tienda"
    ]
    if not all(col in df.columns for col in columnas_requeridas):
        st.error("❌ Faltan columnas necesarias.")
        st.code(columnas_requeridas)
        return

    df["Fecha"] = pd.to_datetime(df["Fecha"])
    df["Margen"] = df["Precio_Venta"] - df["Precio_Compra"]

    tipo_agrupacion = st.radio("Selecciona qué deseas agrupar:", 
                               ["Producto", "Cliente", "Tienda"], horizontal=True)

    if tipo_agrupacion == "Producto":
        grupo = "Nombre_Producto"
        variables_posibles = {
            "Promedio_Ventas": ("Ventas_Unidades", "mean"),
            "Desviacion_Ventas": ("Ventas_Unidades", "std"),
            "Frecuencia": ("Ventas_Unidades", lambda x: (x > 0).sum()),
            "Margen_Promedio": ("Margen", "mean")
        }

    elif tipo_agrupacion == "Cliente":
        grupo = "ID_Cliente"
        variables_posibles = {
            "Promedio_Compra": ("Ventas_Unidades", "mean"),
            "Frecuencia_Compra": ("Ventas_Unidades", lambda x: (x > 0).sum()),
            "Margen_Promedio": ("Margen", "mean"),
            "Diversidad_Productos": ("Nombre_Producto", pd.Series.nunique)
        }

    elif tipo_agrupacion == "Tienda":
        grupo = "Tienda"
        variables_posibles = {
            "Total_Ventas": ("Ventas_Unidades", "sum"),
            "Margen_Promedio": ("Margen", "mean"),
            "Cantidad_Productos": ("Nombre_Producto", pd.Series.nunique),
            "Cantidad_Clientes": ("ID_Cliente", pd.Series.nunique)
        }

    st.markdown(f"📌 Agrupando por **{grupo}** con variables seleccionadas:")

    seleccion_vars = st.multiselect(
        "Selecciona variables para análisis de clúster:",
        list(variables_posibles.keys()),
        default=list(variables_posibles.keys())
    )

    if not seleccion_vars:
        st.warning("⚠️ Selecciona al menos una variable.")
        return

    agregaciones = {var: variables_posibles[var] for var in seleccion_vars}
    agrupado = df.groupby(grupo).agg(**agregaciones).fillna(0)

    if agrupado[seleccion_vars].std().sum() == 0:
        st.warning("⚠️ Las variables seleccionadas no presentan variación. No es posible agrupar.")
        return

    st.dataframe(agrupado)

    # Normalización
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(agrupado)

    # Clustering
    n_clusters = st.slider("Número de clústeres (k):", 2, 10, 3)
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    agrupado["Cluster"] = kmeans.fit_predict(X_scaled)

    st.success("✅ Clusterización completada")

    # Visualización
    eje_x = seleccion_vars[0]
    eje_y = seleccion_vars[1] if len(seleccion_vars) > 1 else seleccion_vars[0]

    fig = px.scatter(
        agrupado,
        x=eje_x,
        y=eje_y,
        color=agrupado["Cluster"].astype(str),
        hover_name=agrupado.index,
        size=agrupado[seleccion_vars[2]] if len(seleccion_vars) > 2 else None,
        title=f"Clústeres de {tipo_agrupacion.lower()}s"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Tabla de entidades con su clúster asignado")
    st.dataframe(agrupado.sort_values("Cluster"))
