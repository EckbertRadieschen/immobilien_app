import streamlit as st
import pandas as pd

def listenfunktion(immobilien):
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
            placeholder = "Städte auswählen"
        )

        min_preis = int(immobilien_df["Preis"].min())
        max_preis = int(immobilien_df["Preis"].max())
        preisbereich = st.slider(
            "Preisbereich",
            min_value = min_preis,
            max_value = max_preis,
            value = (min_preis, max_preis),
            step = 10000
        )

    with filter_columns[2]:
        auswahl_status = st.multiselect(
            "Filter - Status",
            options = ["zu verkaufen", "verkauft"],
            placeholder = "Status auswählen"
        )

        min_flaeche = int(immobilien_df["Fläche"].min())
        max_flaeche = int(immobilien_df["Fläche"].max())
        flaechebereich = st.slider(
            "Fläche-Bereich",
            min_value = min_flaeche,
            max_value = max_flaeche,
            value = (min_flaeche, max_flaeche),
            step = 1
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

    table_column = st.columns([1, 8, 1])
    if len(immobilien_df_gefiltert) < 6:
        table_height = "content"
    else:
        table_height = 248
    with table_column[1]:
        st.markdown("""
            <style>
                .table-container {
                    max-height: 300px;
                    overflow-y: auto;
                    border: 1px solid #444;
                    background-color: #777777;
                    border-radius: 8px
                }

                .table-container table {
                    width: 100%;
                    border-collapse: collapse;
                    color: #eeeeee
                }

                .table-container th {
                    position: sticky;
                    text-align: center;
                    top: 0;
                    background-color: #777777;
                    color: #eeeeee;
                    padding: 8px;
                    z-index: 2;
                    border-bottom: 4px double #eeeeee
                }

                .table-container td {
                    padding: 8px;
                    border-bottom: 1px solid #eeeeee;
                }

                .table-container tr:hover {
                    background-color: #555555;
                } 
                
            </style>
            """, unsafe_allow_html=True)

        st.markdown(
            f"""
                <div class="table-container">
                    {immobilien_df_gefiltert.to_html(index=False)}
                </div>
            """,
            unsafe_allow_html=True
        )