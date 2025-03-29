from textual.app import App, ComposeResult, Screen
from textual.containers import Vertical, Horizontal, Container
from textual.widgets import Input, Button, Label
from home import PublicationScreen
from conexion import vericacion_users, save_usuarios, listar_usuarios
import re

class LoginScreen(Screen):
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
    .ocultar {
        display: none;
    }
    """

    def compose(self) -> ComposeResult:
        self.username_input = Input(placeholder="Nombre de usuario")  # Cambiado de email a username
        self.password_input = Input(placeholder="Contraseña", password=True)
        self.login_message = Label("", id="login_message")
        
        self.new_email_input = Input(placeholder="Correo electrónico (ejemplo@dominio.com)")
        self.new_name_input = Input(placeholder="Nombre completo")  # Cambiado de new_username a new_name
        self.new_username_input = Input(placeholder="Nombre de usuario")  # Nuevo campo para username
        self.new_password_input = Input(placeholder="Contraseña", password=True)
        self.register_message = Label("", id="register_message")
        
        yield Horizontal(
            Container(
                Vertical(
                    Label("Iniciar Sesión"),
                    self.username_input,  # Cambiado de email_input
                    self.password_input,
                    Button("Login", id="login_btn"),
                    self.login_message,
                    id="login_container"
                )
            ),
            Container(
                Vertical(
                    Label("Registro"),
                    self.new_email_input,
                    self.new_name_input,  # Campo para nombre completo
                    self.new_username_input,  # Campo para nombre de usuario
                    self.new_password_input,
                    Button("Registrar", id="new_register_btn"),
                    self.register_message,
                    id="register_container"
                )
            )
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "login_btn":
            username = self.username_input.value
            password = self.password_input.value
            if vericacion_users(username, password):  # Cambiado de email a username
                self.login_message.update("✔️ Login exitoso")
                usuarios = listar_usuarios()
                name = None
                for usuario, data in usuarios.items():
                    if usuario == username:  # Comparar con el username
                        name = data.get('name', username)  # Obtener el nombre completo
                        break
                if name:
                    self.app.switch_screen(PublicationScreen(username, name))  # Pasar username y name
                else:
                    self.login_message.update("❌ Error al obtener datos del usuario")
            else:
                self.login_message.update("❌ Nombre de usuario o contraseña incorrectos")
        
        elif event.button.id == "new_register_btn":
            email = self.new_email_input.value
            name = self.new_name_input.value  # Nombre completo
            username = self.new_username_input.value  # Nombre de usuario
            password = self.new_password_input.value
            self.register_message.update("✔️ Registrando...")
            if email and name and username and password and self.validar_correo(email):
                if save_usuarios(email, name, username, password):  # Pasar todos los campos
                    self.register_message.update(f"✔️ Registro exitoso. Su usuario es: {username}")
                else:
                    self.register_message.update("❌ Nombre de usuario o correo ya registrado")
            else:
                self.register_message.update("❌ Todos los campos son obligatorios o correo inválido")

    def validar_correo(self, email):
        patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(patron, email))

class WeBookApp(App):
    TITLE = "WeBook"

    def on_mount(self) -> None:
        self.push_screen(LoginScreen())