import streamlit as st

# Título de la aplicación
st.title("Subir Archivos con Streamlit")

# Subir archivo
uploaded_file = st.file_uploader("Selecciona un archivo", type=["csv", "xlsx", "txt", "json"])

# Mostrar contenido del archivo subido
if uploaded_file is not None:
    file_details = {
        "Filename": uploaded_file.name,
        "FileType": uploaded_file.type,
        "FileSize": uploaded_file.size
    }
    
    st.write("Detalles del archivo:")
    st.json(file_details)
    
    # Leer y mostrar contenido si es un archivo CSV
    if uploaded_file.type == "text/csv":
        import pandas as pd
        df = pd.read_csv(uploaded_file)
        st.write("Contenido del archivo CSV:")
        st.dataframe(df)
    
    # Leer y mostrar contenido si es un archivo Excel
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(uploaded_file)
        st.write("Contenido del archivo Excel:")
        st.dataframe(df)
    
    # Leer y mostrar contenido si es un archivo de texto
    elif uploaded_file.type == "text/plain":
        string_data = uploaded_file.read().decode("utf-8")
        st.write("Contenido del archivo de texto:")
        st.text(string_data)
    
    # Leer y mostrar contenido si es un archivo JSON
    elif uploaded_file.type == "application/json":
        import json
        json_data = json.load(uploaded_file)
        st.write("Contenido del archivo JSON:")
        st.json(json_data)
else:
    st.write("No se ha subido ningún archivo.")

