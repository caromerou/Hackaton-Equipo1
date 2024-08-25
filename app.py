import streamlit as st
import pandas as pd

# Configuración de usuarios y contraseñas
USERS = {"admin": "123"}  # Puedes añadir más usuarios aquí

def authenticate(username, password):
    return USERS.get(username) == password

def show_login_form():
    st.markdown("""
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background-color: #4CAF50; /* Fondo verde para toda la página */
        }
        .login-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh; /* Altura completa de la ventana del navegador */
            width: 100%;
            position: relative;
        }
        .login-header {
            width: 100%;
            max-width: 600px;
            margin-bottom: 20px;
        }
        .login-header img {
            width: 100%; /* Ancho completo de la imagen */
            height: auto; /* Mantiene la relación de aspecto */
            border-radius: 8px;
        }
        .login-form {
            display: flex;
            flex-direction: column;
            width: 100%;
            max-width: 400px;
            text-align: center;
            padding: 30px;
            border-radius: 12px;
            background-color: #ffffff; /* Fondo blanco para el formulario */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .login-form h2 {
            color: #4CAF50; /* Color verde para el título */
            margin-bottom: 20px;
        }
        .login-form input {
            margin-bottom: 15px;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            width: calc(100% - 24px); /* Ajusta el ancho de los campos de entrada */
        }
        .login-form button {
            padding: 12px;
            border: none;
            border-radius: 8px;
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            cursor: pointer;
            width: 100%; /* Ancho completo del botón */
        }
        .login-form button:hover {
            background-color: #45a049;
        }
        .login-form .message {
            margin-top: 15px;
            font-size: 14px;
        }
        .login-form .error {
            color: #d9534f;
        }
        .login-form .success {
            color: #5bc0de;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-header"><img src="https://bogota.gov.co/sites/default/files/2021-01/uasesp.jpg" alt="UAESP"></div>', unsafe_allow_html=True)
    st.markdown('<div class="login-form">', unsafe_allow_html=True)
    st.markdown('<h2>Inicio de Sesión</h2>', unsafe_allow_html=True)

    username = st.text_input("Nombre de usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar sesión"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.session_state.login_message = "Inicio de sesión exitoso"
        else:
            st.session_state.login_message = "Nombre de usuario o contraseña incorrectos"

    if 'login_message' in st.session_state:
        message_class = 'success' if 'exitoso' in st.session_state.login_message.lower() else 'error'
        st.markdown(f"<p class='message {message_class}'>{st.session_state.login_message}</p>", unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

def show_home_page():
    st.markdown("""
    <style>
        .home-container {
            padding: 20px;
            text-align: center;
        }
        .home-title {
            color: #4CAF50;
            font-size: 36px;
            font-weight: bold;
        }
        .home-content {
            font-size: 18px;
            color: #333;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="home-container">', unsafe_allow_html=True)
    st.markdown('<div class="home-title">Bienvenido a la Aplicación</div>', unsafe_allow_html=True)
    st.markdown('<div class="home-content">', unsafe_allow_html=True)
    st.write("Esta es la página principal de la aplicación. Aquí puedes subir, consultar, editar, eliminar y graficar archivos CSV.")
    st.write("Utiliza la barra de navegación superior para acceder a las diferentes secciones de la aplicación.")
    st.write("¡Espero que disfrutes utilizando la aplicación!")
    st.markdown('</div>', unsafe_allow_html=True)

def show_upload_page():
    st.markdown("""
    <style>
        .upload-container {
            padding: 20px;
        }
        .upload-title {
            color: #4CAF50;
            font-size: 24px;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    st.markdown('<div class="upload-title">Subir Archivo CSV</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")

    if uploaded_file is not None:
        # Lee el archivo CSV en un DataFrame de pandas
        df = pd.read_csv(uploaded_file)
        st.write("Datos cargados:")
        st.write(df.head())
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_edit_page():
    st.markdown("""
    <style>
        .edit-container {
            padding: 20px;
        }
        .edit-title {
            color: #4CAF50;
            font-size: 24px;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="edit-container">', unsafe_allow_html=True)
    st.markdown('<div class="edit-title">Editar Datos</div>', unsafe_allow_html=True)

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

    st.markdown('</div>', unsafe_allow_html=True)

def show_delete_page():
    st.markdown("""
    <style>
        .delete-container {
            padding: 20px;
        }
        .delete-title {
            color: #4CAF50;
            font-size: 24px;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="delete-container">', unsafe_allow_html=True)
    st.markdown('<div class="delete-title">Eliminar Datos</div>', unsafe_allow_html=True)

    if not st.session_state.df.empty:
        delete_index = st.number_input("Número de índice para eliminar", min_value=0, max_value=len(st.session_state.df)-1, step=1)
        if st.button("Eliminar fila"):
            st.session_state.df = st.session_state.df.drop(delete_index).reset_index(drop=True)
            st.success("Fila eliminada exitosamente!")
            st.write("Aquí está el DataFrame actualizado:")
            st.write(st.session_state.df)

    st.markdown('</div>', unsafe_allow_html=True)

def show_visualize_page():
    st.markdown("""
    <style>
        .visualize-container {
            padding: 20px;
        }
        .visualize-title {
            color: #4CAF50;
            font-size: 24px;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="visualize-container">', unsafe_allow_html=True)
    st.markdown('<div class="visualize-title">Visualizar Datos</div>', unsafe_allow_html=True)

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
    
    st.markdown('</div>', unsafe_allow_html=True)

# Inicializa el estado de sesión
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()

if 'page' not in st.session_state:
    st.session_state.page = "home"

# Contenido de la aplicación
if st.session_state.authenticated:
    st.markdown("""
    <style>
        .nav-bar {
            display: flex;
            justify-content: space-between;
            padding: 10px;
            background-color: #4CAF50;
            color: white;
        }
        .nav-bar a {
            color: white;
            text-decoration: none;
            margin: 0 15px;
            font-weight: bold;
        }
        .nav-bar a:hover {
            text-decoration: underline;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
    st.markdown('<a href="javascript:window.location.reload();">Inicio</a>', unsafe_allow_html=True)
    st.markdown('<a href="?page=upload">Subir Archivo</a>', unsafe_allow_html=True)
    st.markdown('<a href="?page=edit">Editar Datos</a>', unsafe_allow_html=True)
    st.markdown('<a href="?page=delete">Eliminar Datos</a>', unsafe_allow_html=True)
    st.markdown('<a href="?page=visualize">Visualizar Datos</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    query_params = st.experimental_get_query_params()
    page = query_params.get("page", ["home"])[0]

    if page == "home":
        show_home_page()
    elif page == "upload":
        show_upload_page()
    elif page == "edit":
        show_edit_page()
    elif page == "delete":
        show_delete_page()
    elif page == "visualize":
        show_visualize_page()
else:
    show_login_form()
