from typing import List, Dict

def build_system_prompt(role_instructions: str) -> str:
    base = (
        "Sos un chatbot de consola que respone en español de forma clara y util. "
        "Si el usuario pide codigo, inclui explicaciones breves. "
        "Evita informacion inventada y pedi aclaraciones si faltan datos.\n\n"
    )
    return base + f"Contexto de rol: {role_instructions}"

def collapse_history(history: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return history