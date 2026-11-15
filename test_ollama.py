
from langchain_ollama import ChatOllama
from langchain.tools import tool


@tool
def get_orders_count():
    """Retourne le nombre de commandes de l'utilisateur."""
    print("--- TOOL APPELÉ ---")
    return 12


llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

llm_with_tools = llm.bind_tools([
    get_orders_count
])

response = llm_with_tools.invoke(
    "Combien de commandes ai-je passées ? Utilise obligatoirement l'outil get_orders_count."
)

print("Réponse du modèle :")
print(response)

print("Appels de Tools :")
print(response.tool_calls)

if response.tool_calls:
    for call in response.tool_calls:
        if call["name"] == "get_orders_count":
            result = get_orders_count.invoke(call["args"])
            print("Résultat de l'outil :", result)