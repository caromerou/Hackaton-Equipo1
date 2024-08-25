import streamlit as st
import pandas as pd

# Título de la aplicación
st.markdown("""
<style>
    .title {
        color: #4CAF50;
        font-size: 36px;
        font-weight: bold;
    }
    .header {
        color: #333;
        font-size: 24px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">App para subir, consultar, editar, eliminar y graficar archivos CSV</div>', unsafe_allow_html=True)

# Barra de navegación
st.sidebar.header("Navegación")
page = st.sidebar.radio("Selecciona una sección:", ["Inicio", "Editar Datos", "Eliminar Datos", "Visualizar Datos"])

# Carga del archivo
uploaded_file = st.sidebar.file_uploader("Elige un archivo CSV", type="csv")

# Inicializa el DataFrame en el estado de sesión
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()

if uploaded_file is not None:
    # Lee el archivo CSV en un DataFrame de pandas
    st.session_state.df = pd.read_csv(uploaded_file)
    st.session_state.file_name = uploaded_file.name

# Inicio
if page == "Inicio":
    st.header("Bienvenido")
    st.write("Sube un archivo CSV y usa las opciones en el menú de la barra lateral para editar, eliminar o visualizar datos.")
    if not st.session_state.df.empty:
        st.write("Datos cargados de:", st.session_state.file_name)
        st.write("Aquí están los primeros 5 registros del archivo:")
        st.write(st.session_state.df.head())
        if st.checkbox("Mostrar el DataFrame completo"):
            st.write(st.session_state.df)

# Editar Datos
elif page == "Editar Datos":
    st.header("Editar Datos")
    if not st.session_state.df.empty:
        edit_index = st.number_input("Número de índice para editar", min_value=0, max_value=len(st.session_state.df)-1, step=1)
        edited_row = st.session_state.df.iloc[edit_index]
        st.write("Fila actual:")
        st.write(edited_row)
        
        # Campos para editar
        new_values = {}
        for col in st.session_state.df.columns:
            new_value = st.text_input(f"Nuevo valor para '{col}'", value=edited_row[col])
            new_values[col] = new_value
        
        if st.button("Actualizar fila"):
            st.session_state.df.loc[edit_index] = new_values
            st.success("Fila actualizada exitosamente!")
            st.write(st.session_state.df.iloc[edit_index])

# Eliminar Datos
elif page == "Eliminar Datos":
    st.header("Eliminar Datos")
    if not st.session_state.df.empty:
        delete_index = st.number_input("Número de índice para eliminar", min_value=0, max_value=len(st.session_state.df)-1, step=1)
        if st.button("Eliminar fila"):
            st.session_state.df = st.session_state.df.drop(delete_index).reset_index(drop=True)
            st.success("Fila eliminada exitosamente!")
            st.write("Aquí está el DataFrame actualizado:")
            st.write(st.session_state.df)

# Visualizar Datos
elif page == "Visualizar Datos":
    st.header("Visualizar Datos")
    if not st.session_state.df.empty and st.checkbox("Mostrar gráfico"):
        x_col = st.selectbox("Selecciona columna para el eje X", st.session_state.df.columns)
        y_col = st.selectbox("Selecciona columna para el eje Y", st.session_state.df.columns)
        
        if x_col and y_col:
            # Verifica que la columna del eje Y sea numérica
            if pd.api.types.is_numeric_dtype(st.session_state.df[y_col]):
                try:
                    st.line_chart(st.session_state.df.set_index(x_col)[y_col])
                except KeyError as e:
                    st.error(f"Error al generar el gráfico: {e}")
            else:
                st.error("La columna seleccionada para el eje Y no es numérica.")
        else:
            st.warning("Selecciona columnas válidas para el gráfico.")


