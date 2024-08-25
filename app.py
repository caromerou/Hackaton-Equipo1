import streamlit as st
import pyexcel as p

# Título de la aplicación
st.title("Subir Archivos con Streamlit usando pyexcel")

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
        csv_data = uploaded_file.read().decode("utf-8")
        st.write("Contenido del archivo CSV:")
        st.text(csv_data)
    
    # Leer y mostrar contenido si es un archivo Excel usando pyexcel
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        # Leer el archivo Excel usando pyexcel
        sheet = p.get_sheet(file_type='xlsx', file_content=uploaded_file.read())
        data = sheet.to_array()
        st.write("Contenido del archivo Excel:")
        st.table(data)
    
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
else:
    st.write("No se ha subido ningún archivo.")

        
        
            
