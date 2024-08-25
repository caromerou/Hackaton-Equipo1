import streamlit as st
import pandas as pd

# Título de la aplicación
st.title('Sube y Visualiza tu Archivo')

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

    
    
       
