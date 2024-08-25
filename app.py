import streamlit as st
import pandas as pd

# Configuración de usuarios y contraseñas
USERS = {"admin": "123"}  # Puedes añadir más usuarios aquí

def authenticate(username, password):
    return USERS.get(username) == password

# Función para mostrar el formulario de inicio de sesión
def show_login_form():
    st.markdown("""
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
        }
        .login-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;  /* Altura completa de la ventana del navegador */
            background-color: #f7f7f7;
        }
        .login-form {
            display: flex;
            flex-direction: column;
            width: 100%;
            max-width: 400px;
            text-align: center;
            padding: 30px;
            border-radius: 10px;
            background-color: #ffffff;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .login-form h2 {
            color: #4CAF50;
            margin-bottom: 20px;
        }
        .login-form input {
            margin-bottom: 15px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        .login-form button {
            padding: 10px;
            border: none;
            border-radius: 5px;
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            cursor: pointer;
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
    
    st.markdown('<div class="login-container"><div class="login-form">', unsafe_allow_html=True)
    
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

# Verifica si el usuario está autenticado
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

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

else:
    # Muestra el formulario de inicio de sesión estilizado
    show_login_form()
