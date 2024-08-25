import streamlit as st
import pandas as pd
import plotly.express as px

# Título de la aplicación
st.title('Sube, Edita, Elimina y Visualiza tu Archivo')

# Carga del archivo
uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")

if uploaded_file is not None:
    # Lee el archivo CSV en un DataFrame de pandas
    df = pd.read_csv(uploaded_file)

    # Muestra el DataFrame original
    st.write("Aquí están los datos originales del archivo:")
    st.write(df)

    # Sección para editar datos
    st.write("Edita los datos:")
    edited_df = st.data_editor(df)

    # Opción para eliminar filas
    st.write("Selecciona las filas que deseas eliminar:")
    selected_rows = st.multiselect('Selecciona las filas a eliminar', list(edited_df.index))

    if selected_rows:
        edited_df = edited_df.drop(selected_rows)
        st.write("Filas eliminadas. Aquí está el DataFrame actualizado:")
        st.write(edited_df)

    # Botón para guardar el DataFrame editado
    if st.button('Guardar Cambios'):
        # Guardar el DataFrame editado en un nuevo archivo CSV
        edited_df.to_csv('archivo_editado.csv', index=False)
        st.success("Cambios guardados exitosamente en 'archivo_editado.csv'.")

    # Consolidar la nueva información en un gráfico
    if st.button('Mostrar Gráfico'):
        # Asegúrate de que el DataFrame tiene datos para graficar
        if not edited_df.empty:
            # Ejemplo: Crear un gráfico de barras de una columna numérica (ajusta según tus datos)
            if 'Número' in edited_df.columns:
                fig = px.bar(edited_df, x=edited_df.index, y='Número', title='Distribución de la columna "Número"')
                st.plotly_chart(fig)
            else:
                st.warning('No se encontró una columna numérica para graficar.')
        else:
            st.warning('El DataFrame está vacío, no se puede generar el gráfico.')

    
    
       
