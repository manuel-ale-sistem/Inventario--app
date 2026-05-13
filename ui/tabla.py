import streamlit as st
import pandas as pd


def mostrar_tabla(df):
    if df.empty:
        st.info("No hay registros para mostrar.")
    else:
        st.dataframe(df, use_container_width=True)

