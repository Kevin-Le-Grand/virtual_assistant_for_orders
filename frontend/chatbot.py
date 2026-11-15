
import streamlit as st
import requests

st.set_page_config(
    page_title="Connexion",
    page_icon="🔐",
    layout="centered"
)

st.title("Bienvenue")
st.subheader("Connectez-vous à votre espace")

with st.form("login_form"):

    email = st.text_input("Email")
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")

    submitted = st.form_submit_button(
        "Se connecter",
        use_container_width=True
    )

    if submitted:

        if not email or not nom or not prenom:
            st.warning("Veuillez remplir tous les champs.")

        else:
            try:
                url = "http://localhost:5000/api/auth/login"

                payload = {
                    "email": email,
                    "nom": nom,
                    "prenom": prenom
                }

                response = requests.post(
                    url,
                    json=payload,
                    timeout=10
                )

                if response.status_code == 200:

                    data = response.json()

                    # Stockage du JWT
                    st.session_state["access_token"] = data["access_token"]

                    # Stockage utilisateur
                    st.session_state["user"] = data["user"]

                    # Redirection
                    st.switch_page("pages/1_Accueil.py")

                else:
                    error = response.json().get(
                        "error",
                        "Erreur lors de la connexion"
                    )
                    st.error(error)

            except requests.exceptions.RequestException as e:
                st.error(f"Erreur API : {e}")
