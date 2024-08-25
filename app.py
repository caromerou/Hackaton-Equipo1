import streamlit as st
import pandas as pd

# Título de la aplicación
st.title('Sube, Edita y Visualiza tu Archivo')

# Carga del archivo
uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")

# Verifica si se ha subido un archivo
if uploaded_file is not None:
    # Lee el archivo CSV en un DataFrame de pandas
    df = pd.read_csv(uploaded_file)
    
    # Muestra los primeros 5 registros del DataFrame
    st.write("Aquí están los primeros 5 registros del archivo:")
    st.write(df.head())
    
    # Muestra el DataFrame completo (opcional, puede ser muy grande)
    if st.checkbox("Mostrar el DataFrame completo"):
        st.write(df)
    
    # Funcionalidad para editar datos
    st.subheader("Editar Datos")
    edit_index = st.number_input("Número de índice para editar", min_value=0, max_value=len(df)-1, step=1)
    if st.button("Editar fila"):
        edited_row = df.iloc[edit_index]
        st.write("Fila actual:")
        st.write(edited_row)
        
        # Campos para editar
        new_values = {}
        for col in df.columns:
            new_values[col] = st.text_input(f"Nuevo valor para '{col}'", value=edited_row[col])
        
        # Actualiza el DataFrame
        if st.button("Actualizar fila"):
            df.loc[edit_index] = new_values
            st.write("Fila actualizada:")
            st.write(df.iloc[edit_index])
    
    # Funcionalidad para eliminar datos
    st.subheader("Eliminar Datos")
    delete_index = st.number_input("Número de índice para eliminar", min_value=0, max_value=len(df)-1, step=1)
    if st.button("Eliminar fila"):
        df = df.drop(delete_index).reset_index(drop=True)
        st.write("Fila eliminada. Aquí está el DataFrame actualizado:")
        st.write(df)
    
    # Consolidar datos en un gráfico
    st.subheader("Visualizar Datos")
    if st.checkbox("Mostrar gráfico"):
        # Aquí puedes elegir qué columnas usar para el gráfico
        x_col = st.selectbox("Selecciona columna para el eje X", df.columns)
        y_col = st.selectbox("Selecciona columna para el eje Y", df.columns)
        
        # Graficar usando Streamlit
        if x_col and y_col:
            st.line_chart(df.set_index(x_col)[y_col])

    
    
       
