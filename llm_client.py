import time
from typing import Dict, List, Optional
import google.generativeai as genai
from config import settings

class GeminiClient:
    def __init__(self, api_key: str, model_name: str):
        if not api_key:
            raise ValueError("GEMINI_API_KEY no esta configurada.")
        genai.configure(api_key=api_key)

        # Descubrir modelos disponibles y elegir uno compatible con generateContent
        try:
            available = list(genai.list_models())
        except Exception as e:
            # Si por alguna razón falla el listado, caemos al modelo solicitado directamente
            print("No se pudo listar modelos de Gemini:", e)
            self.model = genai.GenerativeModel(model_name)
        else:
            # Filtrar los que soportan generateContent
            supported = [
    m for m in available 
    if "generateContent" in getattr(m, "supported_generation_methods", [])
]


            supported_names = [getattr(m, "name", "") for m in supported]

            # Normalizar nombres: la API expone 'models/<nombre>'
            def short(n: str) -> str:
                return n.split("/")[-1] if n else n

            requested_short = short(model_name)

            # ¿El solicitado está disponible?
            chosen = None
            for n in supported_names:
                if short(n) == requested_short:
                    chosen = n
                    break

            # Si no, elegir por preferencia conocida
            if not chosen and supported_names:
                preference = [
                    "gemini-1.5-flash",
                    "gemini-1.5-pro",
                    "gemini-1.0-pro",
                    "gemini-pro",
                ]
                for pref in preference:
                    match = next((n for n in supported_names if short(n) == pref), None)
                    if match:
                        chosen = match
                        break
                # Si sigue sin haber match, tomar el primero soportado
                if not chosen:
                    chosen = supported_names[0]

            chosen_short = short(chosen) if chosen else requested_short
            if chosen and short(chosen) != requested_short:
                print(f"[Gemini] Modelo '{requested_short}' no disponible; usando '{chosen_short}'.")
                print("[Gemini] Modelos disponibles (generateContent):", ", ".join(sorted({short(n) for n in supported_names})))
            else:
                print(f"[Gemini] Usando modelo: {chosen_short}")

            self.model = genai.GenerativeModel(chosen_short)
    def generate(
        self,
        system_prompt: str,
        history: List[Dict[str, str]],
        user_message: str,
        max_retries: int,
        timeout_seconds: int
    ) -> str:
        """
        Manejo de errores con reintentos y backoff exponencial simple.
        """
        attempt = 0
        last_error: Optional[Exception] = None

        # Preparamos el historal como una conversacion del SDK
        # Usamos start_chat para mantener contexto interno con el modelo
        # Pasamos system_prompt como primer mensaje del "usuario" para el rol.
        # (Gemini no tiene "system" estricto, pero ese patron funciona bien)
        convo = self.model.start_chat(history=[{"role": "user", "parts":
        system_prompt}] +
                                              [{"role": m["role"], "parts": [{"text": m["content"]}]} for m in history])
        while attempt < max_retries:
            try:
                # timeouts no estan expuestos directamente; se controla por red.
                response = convo.send_message(user_message)
                text = getattr(response, "text", "")
                if not text:
                    raise RuntimeError("Respuesta vacia del modelo.")
                return text
            except Exception as e:
                last_error = e
                sleep_s = 2 ** attempt # 1,2,4...
                time.sleep(sleep_s)
                attempt += 1

        raise RuntimeError(f"Fallo tras {max_retries} reintentos, Ultimo error:{last_error}")

