import firebase_admin
from firebase_admin import credentials, db
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Input, Static, ListView, ListItem
from textual.containers import Vertical, Horizontal
from textual.events import Click
import os
import json
from datetime import datetime

# Configuración de Firebase
CREDENCIALES_PATH = "credenciales.json"
DATABASE_URL = "https://scrum-c1f2c-default-rtdb.firebaseio.com/"

def inicializar_firebase():
    """Inicializa la conexión con Firebase si no está ya inicializada."""
    if not os.path.exists(CREDENCIALES_PATH):
        credenciales_default = {
            "type": "service_account",
            "project_id": "tu-proyecto-id",
            "private_key_id": "xxxxx",
            "private_key": "-----BEGIN PRIVATE KEY-----\nXXXXXX\n-----END PRIVATE KEY-----\n",
            "client_email": "firebase-adminsdk-xxxxx@tu-proyecto-id.iam.gserviceaccount.com",
            "client_id": "xxxxx"
        }
        with open(CREDENCIALES_PATH, "w") as f:
            json.dump(credenciales_default, f, indent=4)
        print("[!] Se creó un archivo de credenciales por defecto. Reemplázalo con tus credenciales reales.")
        exit(1)

    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(CREDENCIALES_PATH)
            app = firebase_admin.initialize_app(cred, {'databaseURL': DATABASE_URL})
            print(f"[DEBUG] Firebase inicializado con éxito para {app.name}")
    except Exception as e:
        print(f"[!] Error al inicializar Firebase: {e}")
        exit(1)

# Módulo para la interfaz de gestión y publicación
class GestionPublicacion(App):
    """Interfaz de Textual para WeBook con publicaciones, Me gusta y comentarios.
    
    Versión Estrella Fugaz - Ajuste Botón con Texto Adaptable (Restaurar Funcionalidad con Static) ✨
    - Interfaz superior ajustada: botón Ver Lista de Usuarios al lado izquierdo de "¿Qué está pasando?".
    - Botones Me gusta y Comentar como Static con texto, ajustados al tamaño del texto.
    - Restaurada la funcionalidad de clics usando Static y on_click a nivel de la aplicación.
    - Corrección: evita errores al hacer clic en el Input.
    - Espaciado compacto y funcionalidad completa (publicar scribs, dar Me gusta, comentar).
    - Creado con mucho cariño y esfuerzo para cumplir con los requisitos del usuario.
    """
    
    TITLE = "WeBook"
    
    CSS = """
    Static { 
        width: 100%;  /* Asegurar visibilidad */
        padding: 0 1;  /* Reducir padding */
        margin: 0;  /* Mantener espaciado compacto */
        background: transparent;  /* Fondo transparente */
    }
    ListView { 
        height: auto; 
        max-height: 20; 
        border: solid white; 
        padding: 0;  /* Reducir padding */
        background: transparent;  /* Fondo transparente */
    }
    ListItem { 
        height: auto;  /* Ajustar al contenido */
        padding: 0 1;  /* Reducir padding */
        margin: 0;  /* Eliminar márgenes */
        background: transparent;  /* Fondo transparente */
    }
    Input { 
        margin: 1;  /* Asegurar visibilidad */
        width: 50%; 
        height: auto;  /* Ajustar altura */
    }
    Button { 
        margin: 1;  /* Asegurar visibilidad */
        height: auto;  /* Ajustar altura */
    }
    Horizontal { 
        align: left middle;  /* Alinear elementos horizontalmente */
        height: auto;  /* Ajustar altura */
        margin: 0;  /* Mantener espaciado compacto */
    }
    Vertical { 
        height: auto;  /* Ajustar altura */
        margin: 0;  /* Mantener espaciado compacto */
    }
    #publicaciones { margin-top: 1; }
    #usuario_actual { 
        color: white; 
        margin-bottom: 1;  /* Añadir espacio debajo para evitar superposición */
    }
    #btn_publicar { 
        background: #F5F5DC !important; 
        color: black !important; 
        width: 8; 
    }
    #btn_lista_usuarios { 
        background: #F5F5DC !important; 
        color: black !important; 
        width: 15;  /* Ajustar ancho para el texto */
    }
    .like-button { 
        background: #F5F5DC;  /* Fondo igual que Scrib */
        color: black;  /* Color igual que Scrib */
        width: auto;  /* Ajustar al tamaño del texto */
        height: 1; 
        padding: 0 1;
    }
    .like-button:hover { 
        background: #FF5555; 
        color: white; 
    }
    .comment-button { 
        background: #F5F5DC;  /* Fondo igual que Scrib */
        color: black;  /* Color igual que Scrib */
        width: auto;  /* Ajustar al tamaño del texto */
        height: 1; 
        padding: 0 1;
    }
    .comment-button:hover { 
        background: #55FF55; 
        color: black; 
    }
    #comment_input { 
        display: none; 
        width: 70%; 
        height: auto; 
    }
    #submit_comment { 
        display: none; 
        width: 8; 
        height: auto; 
        background: #F5F5DC !important; 
        color: black !important; 
    }
    #btn_volver { 
        margin-top: 1;  /* Añadir espacio arriba */
    }
    """

    def __init__(self, usuario, nombre):
        super().__init__()
        self.usuario = usuario  # Nombre de usuario
        self.nombre = nombre    # Nombre completo
        self.post_ids = {}  # Diccionario para mapear índices de ListItem a post_id
        self.current_comment_post_id = None  # Para rastrear la publicación que se está comentando
        inicializar_firebase()

    def compose(self) -> ComposeResult:
        """Composición de la interfaz de WeBook."""
        yield Header()
        yield Vertical(
            Static(f"@{self.usuario} ({self.nombre})", id="usuario_actual"),
            Horizontal(
                Button("Ver Lista de Usuarios", id="btn_lista_usuarios"),
                Input(placeholder="¿Qué está pasando?", id="mensaje_input"),
                Button("Scrib", id="btn_publicar")
            ),
            ListView(id="publicaciones"),  # Lista de publicaciones
            ListView(id="lista_usuarios", classes="hidden"),
            Horizontal(
                Input(placeholder="Escribe un comentario...", id="comment_input"),
                Button("Enviar", id="submit_comment")
            ),
            Button("Volver al Menú", id="btn_volver", variant="warning")
        )
        yield Footer()

    def on_mount(self) -> None:
        """Cargar publicaciones al iniciar y ajustar estilos."""
        self.cargar_publicaciones()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Manejo de eventos de botones."""
        if event.button.id == "btn_publicar":
            self.crear_publicacion()
        elif event.button.id == "btn_lista_usuarios":
            self.listar_usuarios()
        elif event.button.id == "btn_volver":
            self.exit()
        elif event.button.id == "submit_comment":
            self.enviar_comentario()

    def on_click(self, event: Click) -> None:
        """Manejo de clics en los Static que simulan botones."""
        # Obtener el widget que disparó el evento
        widget = event.control if hasattr(event, 'control') else None
        if widget and widget.id:
            if widget.id.startswith("like_"):
                post_id = widget.id.replace("like_", "")
                self.dar_me_gusta(post_id)
            elif widget.id.startswith("comment_"):
                post_id = widget.id.replace("comment_", "")
                self.mostrar_campo_comentario(post_id)

    def crear_publicacion(self):
        """Crear una publicación en Firebase con formato WeBook."""
        mensaje_input = self.query_one("#mensaje_input", Input)
        mensaje = mensaje_input.value.strip()
        if mensaje:
            try:
                ref = db.reference('publicaciones')
                nueva_pub = ref.push()
                hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                nueva_pub.set({
                    'nombre': self.nombre,
                    'usuario': self.usuario,
                    'hora': hora,
                    'mensaje': mensaje,
                    'likes': 0,
                    'liked_by': [],  # Lista para rastrear quién dio Me gusta
                    'comentarios': []
                })
                self.notify("Scrib publicado con éxito!", severity="information")
                mensaje_input.value = ""
                self.cargar_publicaciones()
            except Exception as e:
                self.notify(f"Error al crear publicación: {e}", severity="error")
        else:
            self.notify("El scrib no puede estar vacío.", severity="error")

    def listar_usuarios(self):
        """Listar usuarios registrados desde Firebase."""
        lista = self.query_one("#lista_usuarios", ListView)
        publicaciones = self.query_one("#publicaciones", ListView)
        lista.clear()
        try:
            ref = db.reference('usuarios')
            usuarios = ref.get()
            if usuarios:
                for usuario, datos in usuarios.items():
                    nombre = datos.get('nombre', 'Desconocido')
                    lista.append(ListItem(Static(f"@{usuario} ({nombre})")))
                lista.remove_class("hidden")
                publicaciones.add_class("hidden")
                self.notify("Lista de usuarios actualizada.", severity="information")
            else:
                self.notify("No hay usuarios registrados.", severity="warning")
        except Exception as e:
            self.notify(f"Error al listar usuarios: {e}", severity="error")

    def cargar_publicaciones(self):
        """Cargar y mostrar publicaciones desde Firebase con comentarios."""
        publicaciones = self.query_one("#publicaciones", ListView)
        lista_usuarios = self.query_one("#lista_usuarios", ListView)
        publicaciones.clear()
        self.post_ids.clear()  # Limpiar el diccionario de mapeo
        try:
            ref = db.reference('publicaciones')
            posts = ref.get()
            if posts:
                for index, (post_id, datos) in enumerate(posts.items()):
                    nombre = datos.get('nombre', 'Desconocido')
                    usuario = datos.get('usuario', 'Anon')
                    hora = datos.get('hora', 'Sin fecha')
                    mensaje = datos.get('mensaje', 'Sin mensaje')
                    likes = datos.get('likes', 0)
                    comentarios = datos.get('comentarios', [])
                    # Construir el texto de la publicación
                    scrib_text = f"{nombre} @{usuario} · {hora}\n{mensaje} ({likes} Me gusta)"
                    # Añadir comentarios si existen
                    if comentarios:
                        for comentario in comentarios:
                            scrib_text += f"\n└ {comentario['autor']}: {comentario['contenido']}"
                    scrib = Static(scrib_text)
                    like_button = Static("Me gusta", id=f"like_{post_id}", classes="like-button")
                    comment_button = Static("Comentar", id=f"comment_{post_id}", classes="comment-button")
                    # Usar Vertical para apilar el texto y los botones
                    publicaciones.append(ListItem(Vertical(
                        scrib,
                        Horizontal(like_button, comment_button)
                    )))
                    self.post_ids[index] = post_id  # Mapear índice a post_id
                publicaciones.remove_class("hidden")
                lista_usuarios.add_class("hidden")
            else:
                publicaciones.append(ListItem(Static("No hay scribs aún.")))
                publicaciones.remove_class("hidden")
                lista_usuarios.add_class("hidden")
            # Ocultar el campo de comentario al recargar
            self.query_one("#comment_input").styles.display = "none"
            self.query_one("#submit_comment").styles.display = "none"
        except Exception as e:
            self.notify(f"Error al cargar publicaciones: {e}", severity="error")

    def dar_me_gusta(self, post_id):
        """Alternar Me gusta en una publicación."""
        try:
            ref = db.reference(f'publicaciones/{post_id}')
            post = ref.get()
            if post:
                liked_by = post.get('liked_by', [])
                current_likes = post.get('likes', 0)
                if self.usuario in liked_by:
                    # Quitar Me gusta
                    liked_by.remove(self.usuario)
                    ref.update({
                        'likes': current_likes - 1,
                        'liked_by': liked_by
                    })
                    self.notify("Me gusta quitado.", severity="information")
                else:
                    # Dar Me gusta
                    liked_by.append(self.usuario)
                    ref.update({
                        'likes': current_likes + 1,
                        'liked_by': liked_by
                    })
                    self.notify("¡Me gusta registrado!", severity="information")
                self.cargar_publicaciones()  # Actualizar la interfaz
            else:
                self.notify("No se encontró la publicación.", severity="error")
        except Exception as e:
            self.notify(f"Error al dar/quitar Me gusta: {e}", severity="error")

    def mostrar_campo_comentario(self, post_id):
        """Mostrar el campo para escribir un comentario."""
        self.current_comment_post_id = post_id
        comment_input = self.query_one("#comment_input")
        submit_button = self.query_one("#submit_comment")
        comment_input.styles.display = "block"
        submit_button.styles.display = "block"
        comment_input.focus()

    def enviar_comentario(self):
        """Enviar un comentario a Firebase."""
        if not self.current_comment_post_id:
            self.notify("No se ha seleccionado una publicación para comentar.", severity="error")
            return

        comment_input = self.query_one("#comment_input", Input)
        comentario = comment_input.value.strip()
        if comentario:
            try:
                ref = db.reference(f'publicaciones/{self.current_comment_post_id}')
                post = ref.get()
                if post:
                    comentarios = post.get('comentarios', [])
                    comentarios.append({
                        'autor': self.nombre,
                        'contenido': comentario,
                        'hora': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    ref.update({'comentarios': comentarios})
                    self.notify("Comentario agregado con éxito!", severity="information")
                    comment_input.value = ""
                    self.query_one("#comment_input").styles.display = "none"
                    self.query_one("#submit_comment").styles.display = "none"
                    self.current_comment_post_id = None
                    self.cargar_publicaciones()
                else:
                    self.notify("No se encontró la publicación.", severity="error")
            except Exception as e:
                self.notify(f"Error al agregar comentario: {e}", severity="error")
        else:
            self.notify("El comentario no puede estar vacío.", severity="error")

# Función para ejecutar el módulo
def ejecutar_gestion_publicacion(usuario, nombre):
    """Iniciar la interfaz de gestión y publicación."""
    app = GestionPublicacion(usuario, nombre)
    app.run()

if __name__ == "__main__":
    # Prueba local
    usuario_prueba = "UsuarioPrueba"
    nombre_prueba = "Usuario Prueba"
    print(f"Simulando sesión con @{usuario_prueba} ({nombre_prueba})")
    ejecutar_gestion_publicacion(usuario_prueba, nombre_prueba)