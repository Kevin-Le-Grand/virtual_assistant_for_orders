# app/services/assistant_service.py

from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from app.tools.order_tools import create_order_tools

# Modèle principal pour les interactions conversationnelles
llm = ChatOllama(
    model="qwen2.5:3b",
    base_url="http://localhost:11434",
    temperature=0,
    num_predict=512
)

# Modèle dédié à la classification : sortie très courte
emotion_llm = ChatOllama(
    model="qwen2.5:3b",
    base_url="http://localhost:11434",
    temperature=0,
    num_predict=3
)

EMOTION_DETECTION_PROMPT = """
Analyse le ton et le contenu du message de l'utilisateur pour déterminer
s'il est en colère ou frustré.

Réponds uniquement par "oui" si l'utilisateur est en colère ou frustré,
sinon réponds par "non".
"""

SUPPORT_EMAIL = "support@votreentreprise.com"

FRUSTRATED_RESPONSE = (
    "Je suis vraiment désolé pour la gêne occasionnée, je comprends votre "
    "frustration. Pour une prise en charge rapide et personnalisée, "
    f"je vous invite à contacter notre support client à l'adresse "
    f"{SUPPORT_EMAIL}."
)

SYSTEM_PROMPT = """
Tu es un assistant conversationnel spécialisé
dans le suivi des commandes clients.

Tu réponds toujours en français.

RÈGLES IMPORTANTES :

1. Utilise les outils pour obtenir les informations provenant de la base de données.
2. Ne fabrique jamais de commandes ou de résultats.
3. N'invente jamais de montants financiers.
4. Utilise get_orders_count pour compter les commandes.
5. Utilise get_orders_statistics pour les statistiques globales.
6. Utilise get_order_by_id pour consulter une commande précise.
7. Si les résultats sont vides, indique-le clairement.

Présente les résultats de manière claire et concise.
"""


def is_user_frustrated(question: str) -> bool:
    """Retourne True si le message exprime de la colère ou de la frustration."""
    response = emotion_llm.invoke(
        [
            {"role": "system", "content": EMOTION_DETECTION_PROMPT},
            {"role": "user", "content": question},
        ]
    )
    return response.content.strip().lower().startswith("oui")


def ask_assistant(question: str, user_id: int):

    # 1. Détection de frustration AVANT l'utilisation des tools
    if is_user_frustrated(question):
        return FRUSTRATED_RESPONSE

    # 2. Sinon, flux normal avec l'agent et ses tools
    tools = create_order_tools(user_id)

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT
    )

    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config={"recursion_limit": 8}
    )

    return result["messages"][-1].content