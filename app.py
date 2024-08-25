import streamlit as st
import pandas as pd

# Configuración de usuarios y contraseñas
USERS = {"admin": "password123"}  # Puedes añadir más usuarios aquí

def authenticate(username, password):
    return USERS.get(username) == password

# Función para mostrar el formulario de inicio de sesión
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
else:
    show_login_form()
