from textual.app import App, ComposeResult
from textual.widgets import Button, Input, Label, Static
from textual.screen import Screen
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class User:
    username: str
    email: str
    password: str

class Database:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.current_user: Optional[User] = None

    def register(self, username: str, email: str, password: str) -> bool:
        if email in [u.email for u in self.users.values()]:
            return False
        self.users[email] = User(username, email, password)
        return True

    def login(self, email: str, password: str) -> bool:
        user = self.users.get(email)
        if user and user.password == password:
            self.current_user = user
            return True
        return False

    def get_users(self) -> Dict[str, User]:
        return self.users.copy()

class LoginScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Label("INICIAR SESIÓN")
        yield Input(placeholder="Email", id="email")
        yield Input(placeholder="Contraseña", id="password", password=True)
        yield Button("Ingresar", id="login")
        yield Button("Registrarse", id="register")
        yield Static("", id="message")

    async def on_button_pressed(self, event: Button.Pressed):
        email = self.query_one("#email", Input).value
        password = self.query_one("#password", Input).value

        if event.button.id == "login":
            if self.app.db.login(email, password):
                self.app.push_screen("menu")
            else:
                self.query_one("#message", Static).update("Credenciales incorrectas")
        elif event.button.id == "register":
            self.app.push_screen("register")

class RegisterScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Label("REGISTRO DE USUARIO")
        yield Input(placeholder="Nombre de usuario", id="username")
        yield Input(placeholder="Email", id="email")
        yield Input(placeholder="Contraseña", id="password", password=True)
        yield Button("Registrar", id="register")
        yield Button("Volver", id="back")
        yield Static("", id="message")

    async def on_button_pressed(self, event: Button.Pressed):
        username = self.query_one("#username", Input).value
        email = self.query_one("#email", Input).value
        password = self.query_one("#password", Input).value

        if event.button.id == "register":
            if self.app.db.register(username, email, password):
                self.query_one("#message", Static).update("Registro exitoso!")
            else:
                self.query_one("#message", Static).update("Email ya registrado")
        elif event.button.id == "back":
            self.app.push_screen("login")

class MenuScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Label(f"BIENVENIDO {self.app.db.current_user.username}")
        yield Static("", id="users_list")
        yield Button("Actualizar lista", id="refresh")
        yield Button("Cerrar sesión", id="logout")

    def on_mount(self):
        self.update_users()

    def update_users(self):
        users = self.app.db.get_users()
        user_list = "\n".join([f"- {u.username} ({u.email})" for u in users.values()])
        self.query_one("#users_list", Static).update(user_list)

    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "refresh":
            self.update_users()
        elif event.button.id == "logout":
            self.app.db.current_user = None
            self.app.push_screen("login")

class RedSocialApp(App):
    SCREENS = {
        "login": LoginScreen,
        "register": RegisterScreen,
        "menu": MenuScreen
    }

    def __init__(self):
        super().__init__()
        self.db = Database()

    def on_mount(self):
        self.push_screen("login")

if __name__ == "__main__":
    app = RedSocialApp()
    app.run()