
import streamlit as st

st.set_page_config(page_title="Accueil")

# Vérification de l'authentification
if "access_token" not in st.session_state:
    st.switch_page("app.py")

# Récupération des données
token = st.session_state["access_token"]
user = st.session_state["user"]

st.title("Bienvenue sur votre espace")

st.write(f"Bonjour {user['username']} !")
st.write("Votre identifiant :", user["id"])
st.write("Votre token :", token)
