# run_front.py
from webapp import create_app 
 
app = create_app() 
 
if __name__ == "__main__": 
    # Debug solo para desarrollo 
    app.run(host="127.0.0.1", port=5000, debug=True) 