from fastapi import APIRouter, HTTPException
from .schemas import chatRequest, chatResponse
from chat_service import ChatService
from roles import RolePreset

router = APIRouter()
chat_service = ChatService(role=RolePreset.ASISTENTE)

@router.post("/chat", response_model=chatResponse)
async def chat_endpoint(request: chatRequest):
    # Validación de contenido
    if not request.mensaje:
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío.")

    # Reset de conversación si corresponde
    if request.reset:
        chat_service.reset()

    # Normalizar rol y mapear a RolePreset
    rol_lower = (request.rol or "").lower()
    mapping = {
        "profesor": RolePreset.PROFESOR,
        "traductor": RolePreset.TRADUCTOR,
        "programador": RolePreset.PROGRAMADOR,
        "asistente": RolePreset.ASISTENTE,
    }
    if rol_lower in mapping:
        chat_service.set_role(mapping[rol_lower])
    else:
        raise HTTPException(status_code=400, detail="Rol inválido. Use profesor|traductor|programador|asistente.")

    # Obtener respuesta del servicio
    try:
        respuesta = chat_service.ask(request.mensaje)
        return chatResponse(respuesta=respuesta)
    except Exception as e:
        import traceback
        print("Error en chat_service.ask:", e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud de chat: {e}")