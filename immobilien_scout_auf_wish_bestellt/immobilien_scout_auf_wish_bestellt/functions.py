import streamlit as st
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE_DIR, "immobilien.json")

def immobilien_suche():
    immobilien = st.session_state.get("immobilienliste", {})
    name = st.session_state.get("suche", None)
    if not name:
        return
    st.session_state.name = name

    data = immobilien[name]

    st.session_state.adresse_aendern = data["Adresse"]
    st.session_state.flaeche_aendern = data["Fläche"]
    st.session_state.preis_aendern = data["Preis"]
    st.session_state.status_aendern = data["Status"]

def immobilienliste_exportieren(immobilienliste):
    with open(path, "w", encoding = "utf-8") as file:
        json.dump(immobilienliste, file, indent=4, ensure_ascii=False)