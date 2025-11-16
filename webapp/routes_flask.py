# webapp/routes.py 
from flask import Blueprint, render_template 
 
ui_bp = Blueprint("ui", __name__, template_folder="templates", static_folder="static") 
 
@ui_bp.get("/") 
def home(): 
    # Página principal del chat 
    return render_template("chat.html")
@ui_bp.get("/about") 
def about(): 
    # Podés sumar una pantalla “Acerca de” si querés 
    return render_template("base.html", content="Acá iría info del proyecto.") 