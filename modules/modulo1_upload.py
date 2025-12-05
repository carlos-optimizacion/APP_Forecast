import streamlit as st
import pandas as pd
import os

def mostrar():
    st.title("📂 Módulo 1: Cargar archivo de ventas")

    # Usar carpeta en minúsculas para compatibilidad con Streamlit Cloud
    carpeta_data = "data"
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

                        # Usar st.rerun() con clave única para evitar bucle con multiselect
                        st.experimental_rerun()

                else:
                    st.error("❌ El archivo no contiene todas las columnas necesarias.")
                    st.code(columnas_requeridas)

            except Exception as e:
                st.error(f"❌ Error al leer el archivo: {e}")


    # --------------------- #
    # 🗑️ Eliminar archivos existentes
    # --------------------- #

    st.subheader("🗃️ Archivos actuales en carpeta 'data'")

    archivos_guardados = sorted([
        f for f in os.listdir(carpeta_data) if f.endswith((".xlsx", ".xls"))
    ])

    if not archivos_guardados:
        st.info("📂 No hay archivos actualmente en la carpeta 'data'.")
        return

    archivos_seleccionados = st.multiselect(
        "Selecciona los archivos que deseas eliminar:",
        archivos_guardados,
        key="seleccion_borrado"
    )

    borrar = st.button("🗑️ Borrar archivos seleccionados", key="boton_borrar")

    if borrar:
        if archivos_seleccionados:
            for archivo in archivos_seleccionados:
                ruta = os.path.join(carpeta_data, archivo)
                try:
                    os.remove(ruta)
                except Exception as e:
                    st.error(f"❌ Error al eliminar {archivo}: {e}")

            st.success("✅ Archivos eliminados correctamente.")
            st.experimental_rerun()
        else:
            st.warning("⚠️ No has seleccionado ningún archivo para eliminar.")
