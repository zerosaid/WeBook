from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, Container
from textual.widgets import Input, Button, Label
import re
from conexion import *
import firebase_admin
from firebase_admin import credentials, firestore
import os


# Credenciales predefinidas

CRED_PATH = "/home/camper/Escritorio/WeBook/WeBook/cred.json"  # Cambiar por la ruta real
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CRED_PATH
cred = credentials.Certificate(CRED_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

class LoginApp(App):
    CSS = """
    #main_container {
        layout: grid;
        grid-columns: 1fr 1fr;
        height: 100%;
        align: center middle;
    }
    
    #login_container, #register_container {
        width: 80%;
        align: center middle;
    }
    
    .btn-crear-cuenta {
        width: 70%;
        background: rgba(5, 5, 5, 0.1);
    }
    .ocultar{
        display:none;
    }
    """
    
    def compose(self) -> ComposeResult:
        self.username_input = Input(placeholder="Usuario")
        self.password_input = Input(placeholder="Contraseña", password=True)
        self.login_message = Label("", id="login_message")
        

        self.email_input = Input(placeholder="Correo")
        self.new_username_input = Input(placeholder="Nombre completo")
        self.new_password_input = Input(placeholder="Nueva Contraseña", password=True)
        self.register_message = Label("", id="register_message")
        
        yield Horizontal(
            Container(
                Vertical(
                    Label("Iniciar Sesión"),
                    self.username_input,
                    self.password_input,
                    Button("Login", id="login_btn"),
                    self.login_message,
                    id="login_container"
                )
            ),
            
            Container(
                Vertical(
                    Label("Registro"),
                    self.email_input,
                    self.new_username_input,
                    self.new_password_input,
                    Button("Registrar", id="new_register_btn"),
                    self.register_message,
                    id="register_container"
                )
            )
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "login_btn":
            usuario = self.username_input.value
            password = self.password_input.value
            
            if vericacion_users(usuario, password):
                self.login_message.update("✔️ Login exitoso")
                #llamar a la rama de montero 
            else:
                self.login_message.update("❌ Usuario o contraseña incorrectos")
            
        elif event.button.id == "new_register_btn":
            email = self.email_input.value
            new_usuario = self.new_username_input.value
            new_password = self.new_password_input.value
            self.register_message.update("✔️ Registrando.....")
            if email and new_usuario and new_password and self.validar_correo(email):
                if save_usuarios(email, new_usuario, new_password):
                    self.register_message.update(f"✔️ Registro exitoso su usario es: {email.split("@")[0].lower()}")
                else:

                    self.register_message.update("❌ Correo ya registrado")

            else:
                self.register_message.update("❌ Todos los campos son obligatorios o correo inavalido")
    def validar_correo(self, email):
        """Verifica si el correo tiene un formato válido"""
        patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(patron, email))            

if __name__ == "__main__":
    LoginApp().run()
