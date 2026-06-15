import streamlit as st
import functions as f
from immobilieneinsicht import listenfunktion
from verwaltung import verwaltungsfunktion
import pandas as pd
import json
import os

# ================================================================
# Aufrufen der Immobilien aus einer JSON-Datei

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE_DIR, "immobilien.json")

if "file_loaded" not in st.session_state:
    with open(path, "r", encoding = "utf-8") as file:
        st.session_state["immobilienliste"] = json.load(file)
        st.session_state["file_loaded"] = 1

# =================================================================

immobilien = st.session_state["immobilienliste"]

if "view" not in st.session_state:
    st.session_state.view = "Hauptmenü"

views = ["Hauptmenü", "Immobilien-Verwaltung", "Immobilien-Liste", "Statistiken"]

columns_header = st.columns([1, 1.7, 1])
with columns_header[1]:
    st.header("WISH - Immobilien")

st.divider()

columns_subheader = st.columns([1, 20])
with columns_subheader[0]:
    st.subheader("→")
with columns_subheader[1]:
    st.subheader(st.session_state.view)

relevant_views = []
for view in views[1:]:
    if st.session_state.view != view:
        relevant_views.append(view)

if st.session_state.view != "Hauptmenü":
    columns_buttons_navigation = st.columns([1.5, 4, 4, 1])
    with columns_buttons_navigation[0]:
        st.write("Navigation:")
    for index, (column, view) in enumerate(zip(columns_buttons_navigation[1:3], relevant_views)):
        with column:
            if st.button(
                view, 
                key = index, 
                width = "stretch"
            ):
                st.session_state.clear()
                st.session_state.view = view
                st.rerun()

st.divider()


# Hauptmenü

if st.session_state.view == "Hauptmenü":
    columns_subheader_hauptmenue = st.columns([1, 1.8, 1])
    with columns_subheader_hauptmenue[1]:
        st.subheader("Treffen Sie ihre Auswahl:")
    
    columns_buttons_hauptmenue = st.columns([1, 4, 4, 4, 1])
    
    for index, (column, view) in enumerate(zip(columns_buttons_hauptmenue[1:4], views[1:])):
        with column:
            if st.button(
                view, 
                key = f"h{index}", 
                width = "stretch"
            ):
                st.session_state.view = view
                st.rerun()
    

# Immobilien verwalten

if st.session_state.view == "Immobilien-Verwaltung":
    verwaltungsfunktion(immobilien)
    

# Immobilien einsehen

if st.session_state.view == "Immobilien-Liste":
    listenfunktion(immobilien)


# Statistiken

if st.session_state.view == "Statistiken":
    liste_subheader_columns = st.columns([1, 1.1, 1])
    with liste_subheader_columns[1]:
        st.subheader("Filter-Optionen")

    immobilien_df = pd.DataFrame.from_dict(
        immobilien,
        orient="index"
    )

    immobilien_df["Stadt"] = (
        immobilien_df["Adresse"]
        .str.split(",")
        .str[-1]
        .str.strip()
    )
    immobilien_df["Adresse"] = (
        immobilien_df["Adresse"]
        .str.split(",")
        .str[0]
        .str.strip()
    )
    immobilien_df = immobilien_df.reindex(columns=["Name", "Adresse", "Stadt", "Fläche", "Preis", "Status"])

    filter_columns = st.columns([3, 1, 3])

    with filter_columns[0]:
        staedte = sorted(immobilien_df["Stadt"].unique())

        auswahl_staedte = st.multiselect(
            "Filter - Stadt",
            options = staedte,
            placeholder = "Städte auswählen",
            key = "auswahl_staedte_stat"
        )

        min_preis = int(immobilien_df["Preis"].min())
        max_preis = int(immobilien_df["Preis"].max())
        preisbereich = st.slider(
            "Preisbereich",
            min_value = min_preis,
            max_value = max_preis,
            value = (min_preis, max_preis),
            step = 10000,
            key = "preisbereich_stat"
        )

    with filter_columns[2]:
        auswahl_status = st.multiselect(
            "Filter - Status",
            options = ["zu verkaufen", "verkauft"],
            placeholder = "Status auswählen",
            key = "auswahl_status_stat"
        )

        min_flaeche = int(immobilien_df["Fläche"].min())
        max_flaeche = int(immobilien_df["Fläche"].max())
        flaechebereich = st.slider(
            "Fläche-Bereich",
            min_value = min_flaeche,
            max_value = max_flaeche,
            value = (min_flaeche, max_flaeche),
            step = 1,
            key = "flaechebereich_stat"
        )

    immobilien_df_gefiltert = immobilien_df.copy()

    if auswahl_staedte:
        immobilien_df_gefiltert = immobilien_df_gefiltert[
            immobilien_df_gefiltert["Stadt"].isin(auswahl_staedte)
        ]

    if auswahl_status:
        immobilien_df_gefiltert = immobilien_df_gefiltert[
            immobilien_df_gefiltert["Status"].isin(auswahl_status)
        ]
    
    immobilien_df_gefiltert = immobilien_df_gefiltert[
        (immobilien_df_gefiltert["Preis"] >= preisbereich[0]) &
        (immobilien_df_gefiltert["Preis"] <= preisbereich[1])        
    ]

    immobilien_df_gefiltert = immobilien_df_gefiltert[
        (immobilien_df_gefiltert["Fläche"] >= flaechebereich[0]) &
        (immobilien_df_gefiltert["Fläche"] <= flaechebereich[1])        
    ]

    st.divider()


    # Statistische Maße

    statistics_columns = st.columns([1, 38, 40, 39, 1])

    with statistics_columns[1]:
        durchschnitt_preis_stat = immobilien_df_gefiltert["Preis"].mean()
        median_preis_stat = immobilien_df_gefiltert["Preis"].median()
        max_preis_stat = immobilien_df_gefiltert["Preis"].max()
        min_preis_stat = immobilien_df_gefiltert["Preis"].min()

        preis_header_columns = st.columns([1, 1.6, 1])
        with preis_header_columns[1]:
            st.subheader("Preis")

        preis_stat_columns = st.columns([1, 3.4, 3, 1])
        with preis_stat_columns[1]:
            st.write("Mittelwert:")
            st.write("Median:")
            st.write("Maximum:")
            st.write("Minimum:")

        with preis_stat_columns[2]:
            st.write(
                f"{durchschnitt_preis_stat:,.0f} €"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )
            st.write(
                f"{median_preis_stat:,g} €"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )
            st.write(
                f"{max_preis_stat:,g} €"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )
            st.write(
                f"{min_preis_stat:,g} €"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

    with statistics_columns[2]:
        durchschnitt_flaeche_stat = immobilien_df_gefiltert["Fläche"].mean()
        median_flaeche_stat = immobilien_df_gefiltert["Fläche"].median()
        max_flaeche_stat = immobilien_df_gefiltert["Fläche"].max()
        min_flaeche_stat = immobilien_df_gefiltert["Fläche"].min()

        flaeche_header_columns = st.columns([1, 2.3, 1])
        with flaeche_header_columns[1]:
            st.subheader("Fläche")

        flaeche_stat_columns = st.columns([1, 3.4, 3, 1])
        with flaeche_stat_columns[1]:
            st.write("Mittelwert:")
            st.write("Median:")
            st.write("Maximum:")
            st.write("Minimum:")

        with flaeche_stat_columns[2]:
            st.write(
                f"{durchschnitt_flaeche_stat:.0f} m²"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )
            st.write(
                f"{median_flaeche_stat:,g} m²"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )
            st.write(
                f"{max_flaeche_stat:,g} m²"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )
            st.write(
                f"{min_flaeche_stat:,g} m²"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

    with statistics_columns[3]:
        eintraege_gesamt = len(immobilien_df_gefiltert)
        anzahl_zu_verkaufen = (immobilien_df_gefiltert["Status"] == "zu verkaufen").sum()
        anteil_zu_verkaufen = anzahl_zu_verkaufen / eintraege_gesamt
        
        anzahl_header_columns = st.columns([1, 13, 1])
        with anzahl_header_columns[1]:
            st.subheader("Verfügbarkeit")

        anzahl_stat_columns = st.columns([1, 20, 8, 1])
        with anzahl_stat_columns[1]:
            st.write("Anzahl Objekte:")
            st.write("Anzahl Verfügbare:")
            st.write("Anteil Verfügbare:")

        with anzahl_stat_columns[2]:
            st.write(
                f"{eintraege_gesamt:,}"
                .replace(",", ".")
            )
            st.write(
                f"{anzahl_zu_verkaufen:,}"
                .replace(",", ".")
            )
            st.write(
                f"{100 * anteil_zu_verkaufen:,.0f} %"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

        
st.markdown("""
    <style>
        .stApp {
            background-color: #f0f2f6;
        }
        
    /* Select-Slider */
        [data-baseweb="slider"] [role="slider"] {
            background-color: #777777 !important;
            border-color: #777777 !important;
        }

        [data-baseweb="slider"] div {
            color: #777777;
            font-size: 14px !important;
            font-weight: 500
        }
            
        [data-baseweb="slider"] {
            --primary-color: #777777 !important;
        }

        [data-baseweb="slider"] [role="presentation"],
        [data-baseweb="slider"] [data-baseweb="track"] {
            background: #777777 !important;
        }

        [data-baseweb="slider"] div[style*="height: 0.25rem"] {
            background: #777777 !important;
            background-color: #777777 !important
        }
            
    /* Multi-Auswahl */
        
        [data-baseweb="select"] > div {
            background-color: #777777 !important;
            border: 1px solid #444 !important;
            font-size: 16px !important;
            font-weight: 500
        }

        [data-baseweb="select"] * {
            color: #eeeeee !important;
        }  

    /* Text-Inputs */

        [data-baseweb="input"] input {
            background-color: #777777;
            color: #eeeeee !important;
            border: 2px solid #444 !important;
            font-size: 16px !important;
            font-weight: 500
        }
        
        /* Wrapper erzwingen (wichtig!) */
        [data-baseweb="input"][aria-disabled="true"] {
            opacity: 1 !important;
            background-color: #777777 !important;
        }

        /* Streamlit fallback wrapper */
        .stTextInput:has(input:disabled) input {
            background-color: #FFFFFF !important
            color: #eeeeee !important;
            -webkit-text-fill-color: #cccccc !important;
            opacity: 1 !important;
        }

        [data-baseweb="input"]:focus-within {
            outline: none !important;
            border: 1px solid #000000 !important;
            box-shadow: none !important;
        }
            
    /* Buttons */
            
        .stButton > button {
            background-color: #777777 !important;
            color: #eeeeee !important;
            border: 1px solid #444 !important;
            border-radius: 6px !important;
        }

        .stButton > button:hover {
            background-color: #666666 !important;
            border-color: #555 !important;
        }

        .stButton > button:active {
            background-color: #555555 !important;
        }
        
        div.stButton > button p {
            font-size: 16px !important;
            font-weight: 500
        }

    </style>
""", unsafe_allow_html=True)


