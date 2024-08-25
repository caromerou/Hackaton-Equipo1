import streamlit as st
import pandas as pd

# Título de la aplicación
st.title('Sube, Edita y Visualiza tu Archivo')

# Carga del archivo
uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")

# Inicializa el DataFrame en el estado de sesión
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()

# Verifica si se ha subido un archivo
if uploaded_file is not None:
    # Lee el archivo CSV en un DataFrame de pandas
    st.session_state.df = pd.read_csv(uploaded_file)
    
    # Muestra los primeros 5 registros del DataFrame
    st.write("Aquí están los primeros 5 registros del archivo:")
    st.write(st.session_state.df.head())
    
    # Muestra el DataFrame completo (opcional, puede ser muy grande)
    if st.checkbox("Mostrar el DataFrame completo"):
        st.write(st.session_state.df)
    
    # Funcionalidad para editar datos
    st.subheader("Editar Datos")
    
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
            st.write("Fila actualizada:")
            st.write(st.session_state.df.iloc[edit_index])
    
    # Funcionalidad para eliminar datos
    st.subheader("Eliminar Datos")
    
    if not st.session_state.df.empty:
        delete_index = st.number_input("Número de índice para eliminar", min_value=0, max_value=len(st.session_state.df)-1, step=1)
        
        if st.button("Eliminar fila"):
            st.session_state.df = st.session_state.df.drop(delete_index).reset_index(drop=True)
            st.write("Fila eliminada. Aquí está el DataFrame actualizado:")
            st.write(st.session_state.df)
    
    # Consolidar datos en un gráfico
    st.subheader("Visualizar Datos")
    
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

