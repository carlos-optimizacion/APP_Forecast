import streamlit as st
import requests
from streamlit_lottie import st_lottie

# Función para cargar animaciones Lottie desde URL
def cargar_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def mostrar():
    # CENTRAR el logo con columnas
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("modules/logo_mi_market.jpeg", width=180)

    # Título del sistema
    st.title("📊 MarketIQ - Inteligencia Comercial para Mi Minimarket")

    # Cargar animación Lottie
    lottie_url = "https://assets2.lottiefiles.com/packages/lf20_yr6zz3wv.json"
    animacion = cargar_lottie_url(lottie_url)

    # CENTRAR la animación usando columnas
    if animacion:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st_lottie(animacion, speed=1, height=250, key="analisis")

    # Sección: ¿Qué es?
    with st.expander("🛒 ¿Qué es MarketIQ?", expanded=True):
        st.markdown("""
        **MarketIQ** es una plataforma de inteligencia de negocios diseñada para 
        negocios de consumo masivo como **Mi Minimarket**. Convierte tus datos de ventas 
        en decisiones estratégicas, gracias a modelos predictivos y segmentación avanzada.
        """)

    # Sección: Funcionalidades clave
    with st.expander("🧠 ¿Qué puedo hacer con esta app?"):
        st.success("✔️ Proyectar demanda con modelos avanzados")
        st.success("✔️ Agrupar productos, tiendas o clientes por comportamiento")
        st.success("✔️ Visualizar resultados con gráficos interactivos")
        st.success("✔️ Cargar tus propios datos en Excel sin programar")

    # Sección: Módulos disponibles
    with st.expander("🧭 Navegación por módulos"):
        st.markdown("""
        | Módulo | Funcionalidad |
        |--------|----------------|
        | **📂 Cargar Datos** | Subida y validación automática de datos de ventas |
        | **📈 Forecast de Ventas** | Proyección de demanda con múltiples modelos (ARIMA, SARIMA, Exponencial) |
        | **📊 Clusterización** | Agrupación estratégica por variables clave |
        """)

    # Llamado a la acción
    st.info("🎯 Usa el menú lateral izquierdo para comenzar el análisis.")
    st.markdown("💬 ¿Dudas o sugerencias? Escríbenos a **carlosnias@gmail.com**")

    # Pie de página
    st.caption("© 2025 MarketIQ para Mi Minimarket – Todos los derechos reservados.")
