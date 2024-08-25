import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Datos de prueba
df = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D'],
    'Value': [10, 20, 15, 25]
})

st.title('Test de Visualización')

# Gráfico de barras de prueba
plt.figure(figsize=(8, 4))
sns.barplot(x='Category', y='Value', data=df, palette='viridis')
plt.title('Gráfico de Barras de Prueba')
st.pyplot()

