import streamlit as st
import pandas as pd
import numpy as np
import os
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
import plotly.graph_objects as go

def forecast_modelos(y):
    resultados = {}
    train = y[:-15]
    test = y[-15:]

    try:
        hw_model = ExponentialSmoothing(train, trend="add", seasonal="add", seasonal_periods=7).fit()
        hw_pred = hw_model.forecast(15)
        resultados["Holt-Winters"] = {
            "modelo": hw_model,
            "pred": hw_pred,
            "mape": mean_absolute_percentage_error(test, hw_pred),
            "rmse": np.sqrt(mean_squared_error(test, hw_pred))
        }
    except:
        resultados["Holt-Winters"] = {"pred": pd.Series(np.nan, index=test.index), "mape": np.nan, "rmse": np.nan}

    try:
        sarima_model = SARIMAX(train, order=(1,1,1), seasonal_order=(1,1,1,7)).fit(disp=False)
        sarima_pred = sarima_model.forecast(15)
        resultados["SARIMA"] = {
            "modelo": sarima_model,
            "pred": sarima_pred,
            "mape": mean_absolute_percentage_error(test, sarima_pred),
            "rmse": np.sqrt(mean_squared_error(test, sarima_pred))
        }
    except:
        resultados["SARIMA"] = {"pred": pd.Series(np.nan, index=test.index), "mape": np.nan, "rmse": np.nan}

    try:
        promedio = train.rolling(window=7).mean().iloc[-1]
        sma_pred = pd.Series(np.full(15, promedio), index=test.index)
        resultados["Prom. Móvil"] = {
            "modelo": promedio,
            "pred": sma_pred,
            "mape": mean_absolute_percentage_error(test, sma_pred),
            "rmse": np.sqrt(mean_squared_error(test, sma_pred))
        }
    except:
        resultados["Prom. Móvil"] = {"pred": pd.Series(np.nan, index=test.index), "mape": np.nan, "rmse": np.nan}

    return resultados, train, test

def mostrar():
    st.title("📈 Módulo 2: Forecast Inteligente de Ventas")

    if not os.path.exists("data"):
        os.makedirs("data")

    archivos = [f for f in os.listdir("data") if f.endswith((".xlsx", ".xls"))]
    if not archivos:
        st.warning("📂 No hay archivos Excel en la carpeta /data.")
        return

    archivo = st.selectbox("Selecciona un archivo de datos:", archivos)
    df = pd.read_excel(os.path.join("data", archivo))

    columnas = ["Fecha", "Categoria", "Nombre_Producto", "Ventas_Unidades"]
    if not all(c in df.columns for c in columnas):
        st.error("❌ Faltan columnas necesarias.")
        st.code(columnas)
        return

    df["Fecha"] = pd.to_datetime(df["Fecha"])
    tipo_analisis = st.radio("Selecciona el tipo de análisis:", ["Producto", "Categoría"])

    def obtener_serie(tipo, categoria=None, producto=None):
        if tipo == "Producto":
            df_fil = df[(df["Categoria"] == categoria) & (df["Nombre_Producto"] == producto)]
            leyenda = f"Producto: {producto}"
        elif tipo == "Categoría":
            df_fil = df[df["Categoria"] == categoria]
            leyenda = f"Categoría: {categoria}"
        else:
            return None, None

        df_ts = df_fil.groupby("Fecha")["Ventas_Unidades"].sum().reset_index().sort_values("Fecha")
        y = df_ts.set_index("Fecha")["Ventas_Unidades"].asfreq("D").fillna(0)
        return y, leyenda

    categoria = None
    producto = None

    if tipo_analisis == "Producto":
        categoria = st.selectbox("Selecciona una categoría:", sorted(df["Categoria"].dropna().unique()))
        productos = df[df["Categoria"] == categoria]["Nombre_Producto"].dropna().unique()
        producto = st.selectbox("Selecciona un producto:", sorted(productos))
    elif tipo_analisis == "Categoría":
        categoria = st.selectbox("Selecciona una categoría:", sorted(df["Categoria"].dropna().unique()))

    y, leyenda = obtener_serie(tipo_analisis, categoria, producto)

    if y is None or len(y) < 40:
        st.warning(f"⚠️ No hay suficientes datos para {leyenda}")
        return

    resultados, train, test = forecast_modelos(y)

    st.subheader("📊 Comparación de Modelos")
    comparacion = pd.DataFrame({
        "Modelo": resultados.keys(),
        "MAPE": [r["mape"] for r in resultados.values()],
        "RMSE": [r["rmse"] for r in resultados.values()]
    })
    st.dataframe(comparacion.round(3))

    modelo_seleccionado = st.selectbox("Selecciona modelo a visualizar:", ["Todos"] + list(resultados.keys()))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=y.index, y=y.values, name="Histórico", mode="lines"))
    fig.add_trace(go.Scatter(x=test.index, y=test.values, name="Test real", mode="lines", line=dict(dash="dot")))

    if modelo_seleccionado == "Todos":
        for nombre, r in resultados.items():
            fig.add_trace(go.Scatter(x=r["pred"].index, y=r["pred"].values, name=nombre, mode="lines"))
    else:
        r = resultados[modelo_seleccionado]
        fig.add_trace(go.Scatter(x=r["pred"].index, y=r["pred"].values, name=modelo_seleccionado, mode="lines"))

    fig.update_layout(title=f"Forecast - {leyenda}", xaxis_title="Fecha", yaxis_title="Unidades")
    st.plotly_chart(fig, use_container_width=True)

    if modelo_seleccionado != "Todos":
        st.subheader("📅 Forecast próximos 30 días")
        fechas = pd.date_range(y.index[-1] + pd.Timedelta(days=1), periods=30)
        if modelo_seleccionado == "Prom. Móvil":
            pred_30 = pd.Series(np.full(30, resultados["Prom. Móvil"]["modelo"]), index=fechas)
        else:
            modelo_final = resultados[modelo_seleccionado]["modelo"]
            pred_30 = modelo_final.forecast(30)
        st.dataframe(pd.DataFrame({"Fecha": fechas, "Forecast": pred_30}))
