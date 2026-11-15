
import streamlit as st
import requests

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Mon Assistant IA",
    page_icon="🤖",
    layout="wide"
)

API_URL = "http://localhost:5000/api/assistant/"

# --------------------------------------------------
# VERIFICATION AUTHENTIFICATION
# --------------------------------------------------

if "access_token" not in st.session_state:
    st.switch_page("app.py")

token = st.session_state["access_token"]
user = st.session_state["user"]

# --------------------------------------------------
# INITIALISATION HISTORIQUE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("🤖 Mon Assistant IA")

    st.write(f"Connecté en tant que : **{user['username']}**")

    st.caption(user["email"])

    st.divider()

    if st.button("➕ Nouvelle conversation", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()

    if st.button("🚪 Déconnexion", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

# --------------------------------------------------
# PAGE PRINCIPALE
# --------------------------------------------------

st.title("Mon Assistant IA")

st.write(
    "Bienvenue ! Posez votre question à votre assistant intelligent."
)

# --------------------------------------------------
# AFFICHAGE HISTORIQUE
# --------------------------------------------------

for message in st.session_state["messages"]:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------------------------------
# ZONE DE SAISIE
# --------------------------------------------------

question = st.chat_input(
    "Posez votre question ici...",
    max_chars=1000
)

if question:

    # Affichage de la question utilisateur
    st.session_state["messages"].append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # --------------------------------------------------
    # APPEL API FLASK
    # --------------------------------------------------

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "question": question
    }

    with st.chat_message("assistant"):

        with st.spinner("Votre assistant réfléchit..."):

            try:

                response = requests.post(
                    API_URL,
                    json=payload,
                    headers=headers,
                    timeout=120
                )

                # Token expiré ou invalide
                if response.status_code == 401:

                    st.session_state.clear()

                    st.error(
                        "Votre session a expiré. "
                        "Veuillez vous reconnecter."
                    )

                    st.switch_page("app.py")

                elif response.status_code == 200:

                    data = response.json()
                    print(data)
                    answer = data.get("answer", "")
                    print(answer)
                    if not answer:
                        answer = "L'assistant n'a retourné aucune réponse."

                    st.markdown(answer)

                    # Enregistrement de la réponse
                    st.session_state["messages"].append({
                        "role": "assistant",
                        "content": answer
                    })

                else:

                    error = response.json().get(
                        "error",
                        "Une erreur est survenue."
                    )

                    st.error(error)

            except requests.exceptions.Timeout:

                st.error(
                    "Le temps de réponse de l'assistant est dépassé."
                )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"Impossible de contacter l'API : {e}"
                )
