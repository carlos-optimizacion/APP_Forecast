import streamlit as st
from modules import (
    modulo0_presentacion,
    modulo1_upload,
    modulo2_forecast,
    modulo3_clusters
)

st.set_page_config(page_title="App de Análisis de Ventas", layout="wide")

# Menú lateral
st.sidebar.title("Menú de Navegación")
opcion = st.sidebar.radio("Selecciona un módulo:", [
    "🏠 Presentación",
    "📂 Cargar Datos",
    "📈 Forecast de Ventas",
    "📊 Clusterización"
])

# Lógica de navegación
if opcion == "🏠 Presentación":
    modulo0_presentacion.mostrar()
elif opcion == "📂 Cargar Datos":
    modulo1_upload.mostrar()
elif opcion == "📈 Forecast de Ventas":
    modulo2_forecast.mostrar()
elif opcion == "📊 Clusterización":
    modulo3_clusters.mostrar()

