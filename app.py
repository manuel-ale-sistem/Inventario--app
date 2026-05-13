import streamlit as st
import pandas as pd
import base64
from datetime import datetime
import getpass

from services.registro_services import (
    cargar_registro,
    guardar_registro,
    validar_campos,
    serie_existe,
    eliminar_registro_por_serie
)

from services.pdf_service import generar_pdf_comodato

from ui.background import set_background
from ui.formulario import formulario_registro
from ui.accesorios import seleccionar_accesorios
from ui.tabla import mostrar_tabla


# ================= CONFIGURACIÓN =================
st.set_page_config(page_title="Registro de Equipos", layout="wide")


# ================= SESSION STATE =================
if "registro" not in st.session_state:
    st.session_state.registro = cargar_registro()


# ================= INTERFAZ =================
set_background("assets/unisys.jpg")

st.markdown('<div class="overlay">', unsafe_allow_html=True)
st.title("📋 Registro de Equipos")


# ---------- FORMULARIO ----------
submit, nuevo = formulario_registro()


# ---------- ACCESORIOS ----------
accesorios = seleccionar_accesorios()


# ---------- GUARDAR REGISTRO ----------
if submit:
    faltantes = validar_campos(nuevo)

    if faltantes:
        st.error(f"Faltan campos: {', '.join(faltantes)}")

    elif serie_existe(st.session_state.registro, nuevo["Serie"]):
        st.error("La serie ya existe en el registro")

    else:
        # Procesar accesorios
        lista_accesorios = []
        for items in accesorios.values():
            lista_accesorios.extend(items)

        nuevo["Accesorios"] = ", ".join(lista_accesorios) if lista_accesorios else "-"
        nuevo["FechaRegistro"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        nuevo["FechaEntrega"] = datetime.now().strftime("%d/%m/%Y")
        nuevo["CapturadoPor"] = getpass.getuser()

        guardar_registro(nuevo)
        st.session_state.registro = cargar_registro()

        st.success("✅ Registro agregado correctamente")


# ---------- TABLA ----------
mostrar_tabla(st.session_state.registro)


# ---------- PDF ----------
st.subheader("📄 Comodato")

if st.button("Generar Comodato PDF"):
    if not st.session_state.registro.empty:
        ultimo_registro = st.session_state.registro.iloc[-1].to_dict()

        st.info(
            f"""
            **Datos del comodato**
            - 👤 Usuario: {ultimo_registro.get("Usuario", "")}
            - 🖥️ Serie: {ultimo_registro.get("Serie", "")}
            - 🎫 RITM: {ultimo_registro.get("RITM", "")}
            """
        )

        buffer = generar_pdf_comodato(
            ultimo_registro,
            ultimo_registro.get("Accesorios", "")
        )

        usuario = ultimo_registro.get("Usuario", "Usuario")
        serie = ultimo_registro.get("Serie", "Serie")
        ritm = ultimo_registro.get("RITM", "RITM")

        nombre_pdf = f"Comodato_{usuario}_{serie}_{ritm}.pdf".replace(" ", "_")

        b64 = base64.b64encode(buffer.read()).decode()
        href = (
            f'<a href="data:application/pdf;base64,{b64}" '
            f'download="{nombre_pdf}">📥 Descargar Comodato PDF</a>'
        )

        st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("No hay registros para generar el PDF.")


# ---------- ELIMINAR REGISTRO ----------
st.subheader("🗑️ Eliminar registro")

if not st.session_state.registro.empty:
    serie_seleccionada = st.selectbox(
        "Selecciona la serie a eliminar",
        st.session_state.registro["Serie"]
    )

    confirmar = st.checkbox(
        "Confirmo que deseo eliminar este registro"
    )

    if confirmar and st.button("Eliminar registro"):
        eliminar_registro_por_serie(serie_seleccionada)
        st.session_state.registro = cargar_registro()
        st.success(f"✅ Registro con serie {serie_seleccionada} eliminado")


st.markdown("</div>", unsafe_allow_html=True)