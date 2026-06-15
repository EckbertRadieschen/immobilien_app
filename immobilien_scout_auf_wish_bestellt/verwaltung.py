import streamlit as st
import functions as f

# Immobilien verwalten
def verwaltungsfunktion(immobilien):

    if "verwaltungsmodus" in st.session_state:
        verwaltung_navi_columns = st.columns([1, 1, 1])
        with verwaltung_navi_columns[1]:
            if "verwaltungsmodus" in st.session_state:
                    if st.button("Zurück zum Verwaltungsmenü"):
                        del st.session_state.verwaltungsmodus
                        if "name" in st.session_state:   
                            del st.session_state.name
                        st.rerun()
        if st.session_state.verwaltungsmodus == "bearbeiten":
            if "name" not in st.session_state:
                verwaltung_subheader_columns = st.columns([1, 2, 1])
                with verwaltung_subheader_columns[1]:
                    st.subheader("Wähle eine Immobilie aus:")
            else: 
                verwaltung_subheader_columns = st.columns([1, 1.5, 1])
                with verwaltung_subheader_columns[1]:
                    st.subheader("Ändern oder Löschen:")
        
        if st.session_state.verwaltungsmodus == "hinzufügen":
            verwaltung_subheader_columns = st.columns([1, 9, 1])
            with verwaltung_subheader_columns[1]:
                st.subheader("Geben Sie die Daten der neuen Immobilie ein:")                

    if "verwaltungsmodus" not in st.session_state:
        verwaltung_subheader_columns = st.columns([1, 2.5, 1])
        with verwaltung_subheader_columns[1]:
            st.subheader("Wähle eine Verwaltungsoption:")

        verwaltungsmodus_columns = st.columns([1, 2, 2, 1])
        with verwaltungsmodus_columns[1]:
            if st.button("Immobilie Hinzufügen", key = "hinzufügen", width = "stretch"):
                st.session_state.verwaltungsmodus = "hinzufügen"
                st.rerun()
        with verwaltungsmodus_columns[2]:
            if st.button("Immobilien bearbeiten", key = "bearbeiten", width = "stretch"):
                st.session_state.verwaltungsmodus = "bearbeiten"
                st.rerun()

# -----------------------------------------------------------------------------------------------
# Verwaltungsoption "hinzufügen"

    if "verwaltungsmodus" in st.session_state:
        if st.session_state.verwaltungsmodus == "hinzufügen":
            immobilien_nummern = []
            for immobilie in immobilien:
                nummer = int(immobilien[immobilie]["Name"][5:].lstrip("0"))
                immobilien_nummern.append(nummer)
            max_immobilien_nummer = max(immobilien_nummern)
            neuer_immobilien_name = f"Immo_{str(max_immobilien_nummer + 1).zfill(2)}"

            st.markdown(
                """
                    <style>
                        [data-baseweb="slider"] div[role="slider"] {
                            background-color: green !important;
                        }
                    </style>
                """, 
                unsafe_allow_html=True
            )
            if "add_valid" not in st.session_state:
                st.session_state.add_valid = None
            add_input_columns = st.columns([1, 2, 1])
            with add_input_columns[1]:
                hinzufuegen_name = st.text_input(
                    "Name", 
                    key = "name_hinzufuegen", 
                    value = neuer_immobilien_name, 
                    disabled = True
                )
                hinzufuegen_adresse = st.text_input(
                    "Adresse", 
                    key = "adresse_hinzufuegen"
                )
                hinzufuegen_flaeche = st.select_slider(
                    "Fläche", 
                    options = range(10, 301, 1),
                    key = "flaeche_hinzufuegen"
                )
                hinzufuegen_preis = st.select_slider(
                    "Preis", 
                    options= range(10000, 1000001, 10000), 
                    key = "preis_hinzufuegen"
                )
                hinzufuegen_status = st.selectbox(
                    "Status", 
                    options = ["verkauft", "zu verkaufen"], 
                    key = "status_hinzufuegen"
                )

            add_button_columns = st.columns([1, 0.75, 1])
            with add_button_columns[1]:
                if st.button("Immobilie hinzufügen"):
                    st.session_state.add_valid = 1

            if st.session_state.add_valid == 1:
                bottom_columns = st.columns([1, 3, 1])
                
                with bottom_columns[1]:
                    st.warning("Wirklich hinzufügen?")
                    hinzufuegen_bestaetigen_columns = st.columns([1, 3, 3, 1])

                    with hinzufuegen_bestaetigen_columns[1]:
                        if st.button("Ja, hinzufügen"):
                            immobilien[neuer_immobilien_name] = {
                                "Name": hinzufuegen_name,
                                "Adresse": hinzufuegen_adresse,
                                "Fläche": hinzufuegen_flaeche,
                                "Preis": hinzufuegen_preis,
                                "Status": hinzufuegen_status
                            }
                            st.session_state.add_valid = None
                            f.immobilienliste_exportieren(immobilien)
                            st.rerun()

                    with hinzufuegen_bestaetigen_columns[2]:
                        if st.button("Abbrechen", key = "hinzufuegen_abbrechen"):
                            st.session_state.add_valid = None
                            st.rerun()

        # -------------------------------------------------------------------------------
        # Verwaltungsoption "bearbeiten"

        if st.session_state.verwaltungsmodus == "bearbeiten":

            il_columns = st.columns([3, 0.5, 3])

            with il_columns[0]:
                st.selectbox(
                    "Immobilie",
                    list(immobilien.keys()),
                    key = "suche",
                    on_change = f.immobilien_suche
                )
                
                if "name" in st.session_state and \
                    st.session_state.name != None and \
                        st.session_state.name in immobilien:
                    actual_data = immobilien[st.session_state.name]

                    st.session_state["Adresse"] = st.text_input(
                        "Adresse", 
                        value = actual_data["Adresse"],
                        key = "adresse_aendern"
                    )
                    st.session_state["Fläche"] = st.select_slider(
                        "Fläche", 
                        options = range(10, 301, 1), 
                        value = actual_data["Fläche"],
                        key = "flaeche_aendern"
                    )
                    st.session_state["Preis"] = st.select_slider(
                        "Preis", 
                        options = range(10000, 1000001, 10000),
                        value = actual_data["Preis"],
                        key = "preis_aendern"
                    )
                    actual_status = actual_data["Status"]
                    optionen = ["verkauft", "zu verkaufen"]

                    st.session_state["Status"] = st.selectbox(
                        "Status", 
                        options = optionen,
                        index = optionen.index(actual_status),
                        key = "status_aendern"
                    )

                    st.divider()

                    if "change_valid" not in st.session_state:
                            st.session_state.change_valid = None

                    uebernehmen_button_columns = st.columns([1, 6, 1])
                    with uebernehmen_button_columns[1]:
                        if st.button("Änderungen übernehmen", key = "übernehmen"):
                            st.session_state.change_valid = 1

                    if st.session_state.change_valid == 1:
                            st.warning("Wirklich übernehmen?")

                            uebernehmen_bestaetigen_columns = st.columns([1.4, 1])

                            with uebernehmen_bestaetigen_columns[0]:
                                if st.button("Ja, übernehmen"):
                                    actual_data["Adresse"] = st.session_state["adresse_aendern"]
                                    actual_data["Fläche"] = st.session_state["flaeche_aendern"]
                                    actual_data["Preis"] = st.session_state["preis_aendern"]
                                    actual_data["Status"] = st.session_state["status_aendern"]
                                    st.session_state.change_valid = None
                                    f.immobilienliste_exportieren(immobilien)
                                    st.rerun()

                            with uebernehmen_bestaetigen_columns[1]:
                                if st.button("Abbrechen", key = "aendern_abbrechen"):
                                    st.session_state.change_valid = None
                                    st.rerun()
                    

                    with il_columns[2]:

                        if st.session_state.name in immobilien:
                            immo_header_columns = st.columns([1, 1.6, 1])
                            with immo_header_columns[1]:
                                st.subheader(st.session_state.name)
                            
                            immo_columns = st.columns([2.25, 5])
                            with immo_columns[0]:
                                st.write("Adresse:")
                                st.write("Fläche:")
                                st.write("Preis:")
                                st.write("Status:")
                            with immo_columns[1]:
                                st.write(f"{actual_data['Adresse']}")
                                st.write(f"{actual_data['Fläche']} m²")
                                st.write(f"{actual_data['Preis']} €")
                                st.write(f"{actual_data['Status']}")
                            
                            st.divider()

            # Löschen Button
                        if "delete_candidate" not in st.session_state:
                            st.session_state.delete_candidate = None

                        loeschen_button_columns = st.columns([1, 3, 1])
                        with loeschen_button_columns[1]:
                            if st.button("Immobilie löschen"):
                                st.session_state.delete_candidate = st.session_state.name
                            
                        if st.session_state.delete_candidate == st.session_state.name:
                            st.warning("Wirklich löschen? Diese Aktion kann nicht rückgängig gemacht werden.")

                            loeschen_bestaetigen_columns = st.columns([1, 3, 3, 1])

                            with loeschen_bestaetigen_columns[1]:
                                if st.button("Ja, löschen"):
                                    del immobilien[st.session_state.name]
                                    st.session_state.delete_candidate = None
                                    st.session_state.name = None
                                    f.immobilienliste_exportieren(immobilien)
                                    st.rerun()

                            with loeschen_bestaetigen_columns[2]:
                                if st.button("Abbrechen", key = "loeschen_abbrechen"):
                                    st.session_state.delete_candidate = None
                                    st.rerun()