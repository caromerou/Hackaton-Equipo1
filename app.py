import streamlit as st
import pandas as pd

# Configuración de usuarios y contraseñas
USERS = {"admin": "password123"}  # Puedes añadir más usuarios aquí

def authenticate(username, password):
    return USERS.get(username) == password

# Función para mostrar el formulario de inicio de sesión
def show_login_form():
    st.sidebar.markdown("""
    <style>
        .login-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;  /* Altura completa de la ventana del navegador */
        }
        .login-form {
            display: flex;
            flex-direction: column;
            width: 100%;
            max-width: 300px;
            text-align: center;
        }
        .login-form input {
            margin-bottom: 10px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown('<div class="login-container"><div class="login-form">', unsafe_allow_html=True)
    
    username = st.sidebar.text_input("Nombre de usuario")
    password = st.sidebar.text_input("Contraseña", type="password")
    
    st.sidebar.markdown('</div></div>', unsafe_allow_html=True)
    
    if st.sidebar.button("Iniciar sesión"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.sidebar.success("Inicio de sesión exitoso")
        else:
            st.sidebar.error("Nombre de usuario o contraseña incorrectos")

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
           
