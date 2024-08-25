import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# Inicializa el estado de sesión
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()

if 'page' not in st.session_state:
    st.session_state.page = "home"

def plot_chart(df, x_col, y_col, chart_type):
    plt.figure(figsize=(10, 6))
    if chart_type == 'Bar':
        df.groupby(x_col)[y_col].sum().plot(kind='bar')
        plt.title(f'Bar Chart of {y_col} vs {x_col}')
    elif chart_type == 'Histogram':
        df[y_col].plot(kind='hist', bins=20)
        plt.title(f'Histogram of {y_col}')
    elif chart_type == 'Frequency Diagram':
        sns.histplot(df[y_col], discrete=True)
        plt.title(f'Frequency Diagram of {y_col}')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    st.pyplot()

if st.session_state.authenticated:
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
    page = st.sidebar.radio("Selecciona una sección:", ["Inicio", "Editar Datos", "Eliminar Datos", "Visualizar Datos", "Subir Archivo"])

    # Carga del archivo
    uploaded_file = st.sidebar.file_uploader("Elige un archivo CSV", type="csv")

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
        if not st.session_state.df.empty:
            chart_type = st.selectbox("Selecciona el tipo de gráfico", ["Bar", "Histogram", "Frequency Diagram"])
            x_col = st.selectbox("Selecciona columna para el eje X", st.session_state.df.columns)
            y_col = st.selectbox("Selecciona columna para el eje Y", st.session_state.df.columns)
            if x_col and y_col:
                plot_chart(st.session_state.df, x_col, y_col, chart_type)
            else:
                st.warning("Selecciona columnas válidas para el gráfico.")

    # Subir Archivo
    elif page == "Subir Archivo":
        st.header("Subir Archivo CSV")
        uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")

        if uploaded_file is not None:
            st.session_state.df = pd.read_csv(uploaded_file)
            st.session_state.file_name = uploaded_file.name
            st.write("Datos cargados:")
            st.write(st.session_state.df.head())

else:
    show_login_form()

