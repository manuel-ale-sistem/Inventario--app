import streamlit as st


def seleccionar_accesorios():
    st.subheader("Accesorios")

    accesorios = {
        "Laptop": ["Cargador", "Mouse", "Mochila"],
        "Celular": ["Cargador", "Cable USB", "Audífonos"],
        "Monitor": ["Cable HDMI", "Cable DisplayPort"]
    }

    seleccionados = {}

    for categoria, lista in accesorios.items():
        seleccion = st.multiselect(
            categoria,
            options=lista
        )
        seleccionados[categoria] = seleccion

    return seleccionados
