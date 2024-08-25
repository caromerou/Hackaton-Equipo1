import streamlit as st
import csv
import json
from io import StringIO, BytesIO

# Título de la aplicación
st.title("Subir Archivos con Streamlit (sin pandas ni openpyxl)")

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
        # Usar csv.reader para leer el archivo CSV
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        reader = csv.reader(stringio)
        csv_data = list(reader)
        st.write("Contenido del archivo CSV:")
        st.table(csv_data)
    
    # Leer y mostrar contenido si es un archivo de texto
    elif uploaded_file.type == "text/plain":
        string_data = uploaded_file.read().decode("utf-8")
        st.write("Contenido del archivo de texto:")
        st.text(string_data)
    
    # Leer y mostrar contenido si es un archivo JSON
    elif uploaded_file.type == "application/json":
        json_data = json.load(uploaded_file)
        st.write("Contenido del archivo JSON:")
        st.json(json_data)
    
    # Leer y mostrar contenido si es un archivo Excel (sin openpyxl)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        # Usar BytesIO para leer el archivo binario
        bytes_data = BytesIO(uploaded_file.read())
        st.write("Contenido del archivo Excel:")
        st.write("Visualización directa no soportada sin `openpyxl`, descarga para ver el contenido.")
        st.download_button(
            label="Descargar archivo Excel",
            data=bytes_data,
            file_name=uploaded_file.name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.write("No se ha subido ningún archivo.")


    
