import streamlit as st
import pandas as pd
import os

def mostrar():
    st.title("📂 Módulo 1: Cargar archivo de ventas")

    # Inicializar variables
    carpeta_data = "Data"
    os.makedirs(carpeta_data, exist_ok=True)

    # --------------------- #
    # 🔼 Subir y guardar archivo
    # --------------------- #

    with st.expander("📤 Subir nuevo archivo Excel", expanded=True):
        archivo = st.file_uploader("Selecciona un archivo Excel:", type=["xlsx", "xls"], key="upload")

        if archivo is not None:
            try:
                df = pd.read_excel(archivo)
                st.success("✅ Archivo cargado correctamente")
                st.dataframe(df.head())

                columnas_requeridas = [
                    'Fecha', 'Dia_del_anio', 'ID_Cliente', 'ID_Producto',
                    'Categoria', 'Descripcion_Producto', 'Nombre_Producto',
                    'Tienda', 'Ventas_Unidades', 'Precio_Compra', 'Precio_Venta'
                ]

                if all(col in df.columns for col in columnas_requeridas):
                    st.success("✅ Todas las columnas requeridas están presentes.")

                    if st.button("📥 Guardar archivo"):
                        ruta = os.path.join(carpeta_data, archivo.name)
                        with open(ruta, "wb") as f:
                            f.write(archivo.getbuffer())
                        st.success(f"Archivo guardado como: {archivo.name}")
                        st.rerun()
                else:
                    st.error("❌ El archivo no contiene todas las columnas necesarias.")
                    st.code(columnas_requeridas)
            except Exception as e:
                st.error(f"❌ Error al leer el archivo: {e}")

    # --------------------- #
    # 🗑️ Eliminar archivos existentes
    # --------------------- #

    st.subheader("🗃️ Archivos actuales en carpeta 'Data'")

    archivos_guardados = sorted([
        f for f in os.listdir(carpeta_data) if f.endswith((".xlsx", ".xls"))
    ])

    if not archivos_guardados:
        st.info("📂 No hay archivos actualmente en la carpeta 'Data'.")
        return

    archivos_seleccionados = st.multiselect(
        "Selecciona los archivos que deseas eliminar:",
        archivos_guardados,
        key="borrar"
    )

    if st.button("🗑️ Borrar archivos seleccionados"):
        if archivos_seleccionados:
            for archivo in archivos_seleccionados:
                ruta = os.path.join(carpeta_data, archivo)
                try:
                    os.remove(ruta)
                except Exception as e:
                    st.error(f"❌ Error al eliminar {archivo}: {e}")
            st.success("✅ Archivos eliminados correctamente.")
            st.rerun()
        else:
            st.warning("⚠️ No has seleccionado ningún archivo para eliminar.")
