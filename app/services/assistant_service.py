
# app/services/assistant_service.py

import os

from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from app.tools.order_tools import create_order_tools

# Initialisation du modèle Ollama
llm = ChatOllama(
    model="qwen2.5:3b",
    base_url="http://localhost:11434",
    temperature=0,
    num_predict=512
)


SYSTEM_PROMPT = """
Tu es un assistant conversationnel spécialisé
dans le suivi des commandes clients.

Tu réponds toujours en français.

Tu disposes de plusieurs outils pour interroger
les commandes de l'utilisateur connecté.

RÈGLES IMPORTANTES :

1. Utilise les outils pour obtenir les informations
   provenant de la base de données.

2. Ne fabrique jamais de commandes ou de résultats.

3. N'invente jamais de montants financiers.
   Tu ne disposes pas des informations financières.

4. Utilise get_orders_count pour compter les commandes.

5. Utilise get_orders_statistics pour les statistiques globales.

6. Utilise get_order_by_id pour consulter une commande précise.

7. Si les résultats sont vides, indique-le clairement.

11. Si un utilisateur te semble enervé ou frustré, réponds avec 
    empathie et propose lui  de contacter le support client par
    email support@votreentreprise.com.

Présente les résultats de manière claire et concise.
"""


def ask_assistant(question: str, user_id: int):

    # Création des outils propres à l'utilisateur
    tools = create_order_tools(user_id)

    # Création de l'agent
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT
    )

    # Exécution de la question
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        },
        config={
            "recursion_limit": 8
        }
    )

    # Récupération du dernier message
    answer = result["messages"][-1].content
    return answer


