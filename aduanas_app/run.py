import webbrowser
import threading
import time
from waitress import serve
from app import app

def open_browser():
    """Abre el navegador después de un breve retraso para asegurar que el servidor esté listo."""
    time.sleep(1.5)
    print("Abriendo el navegador en http://127.0.0.1:5000")
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == '__main__':
    # Iniciar un hilo separado para abrir el navegador
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Iniciar el servidor WSGI de Waitress
    print("Iniciando aplicación Aduanas en el puerto 5000...")
    serve(app, host='127.0.0.1', port=5000)
