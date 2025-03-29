import firebase_config  # Añade esto para asegurar la inicialización
from login_app import WeBookApp

if __name__ == "__main__":
    app = WeBookApp()
    app.run()