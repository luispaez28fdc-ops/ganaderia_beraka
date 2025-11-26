import streamlit as st
import os

st.set_page_config(page_title="Beraka Ganaderia", layout="centered")

if os.path.exists("assets/logo_beraka.png"):
    st.image("assets/logo_beraka.png", width=300)

st.title("Beraka Ganaderia")
st.markdown("### Sistema del campo")

st.markdown("""
- **Rodeo** → inventario completo con gráfico  
- **Sociedad con mi abuelo** → mismo inventario pero sin gráfico (para el abuelo)
""")

st.info("Todo se guarda en la carpeta. Funciona sin internet.")
st.caption("Beraka Ganaderia - Sociedad con el abuelo desde siempre")