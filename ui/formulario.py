import streamlit as st
from config import MODELOS_POR_TIPO

def formulario_registro():

    st.subheader("📋 Datos del Equipo")

    # Widgets FUERA del form (reactivos)
    tipo = st.selectbox(
        "Tipo",
        options=list(MODELOS_POR_TIPO.keys()),
        key="tipo"
    )

    modelo = st.selectbox(
        "Modelo",
        options=MODELOS_POR_TIPO[tipo],
        key="modelo"
    )

    # Formulario SOLO para inputs finales
    with st.form("form_registro"):

        marca = st.selectbox("Marca", ["HP", "Samsung", "Honeywell"])
        estado = st.selectbox("Estado", ["Asignado", "Stock"])
        usuario = st.text_input("Usuario")
        serie = st.text_input("Serie")
        imei = st.text_input("IMEI / Host")
        linea = st.text_input("Línea")
        localidad = st.text_input("Localidad")
        ritm = st.text_input("RITM")

        submit = st.form_submit_button("➕ Agregar Registro")

    return submit, {
    "Modelo": modelo,
    "Serie": serie,
    "Marca": marca,
    "Tipo": tipo,
    "IMEI_HOST": imei,
    "LINEA": linea,
    "LOCALIDAD": localidad,
    "Estado": estado,
    "Usuario": usuario,
    "RITM": ritm
    }