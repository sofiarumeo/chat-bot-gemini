from collections import deque
from typing import Deque, Dict, List

class ConversationMemory:
    def __init__(self, max_messages: int = 12):
        self._messages: Deque[Dict[str, str]] = deque(maxlen=max_message)

    def add_user(self, content: str):
        self._messages.append({"role": "user", "content": content})
    def add_model(self, content: str):
        self._messages.append({"role": "model", "content": content})
    def get(self) -> List[Dict[str, str]]:
        return list(self._messages)
    def clear(self):
        self._messages.clear()