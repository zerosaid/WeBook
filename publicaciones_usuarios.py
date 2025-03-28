import firebase_admin
from firebase_admin import credentials, db
from textual.app import App, ComposeResult
from textual.widgets import Header, Button, Input, Static, ListView, ListItem
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
    """Interfaz de Textual para WeBook con publicaciones, Me gusta y comentarios anidados."""
    
    TITLE = "WeBook"
    
    CSS = """
    Static { 
        padding: 0 1;   /* Reducimos el padding */
        margin: 0;      /* Eliminamos márgenes innecesarios */
        background: transparent; 
        color: white;
    }
    ListView { 
        height: auto;   /* Altura dinámica */
        width: 100%;    /* Ocupa todo el ancho disponible */
        border: solid white; 
        padding: 0;     /* Reducimos el padding */
        background: transparent; 
    }
    ListItem { 
        height: auto;   /* Altura dinámica */
        width: 100%;    /* Ocupa todo el ancho disponible */
        padding: 0 1;   /* Reducimos el padding */
        margin: 0;      /* Eliminamos márgenes */
        background: transparent; 
    }
    Input { 
        margin: 0 1;    /* Reducimos márgenes */
        width: 50%; 
        height: auto; 
    }
    Button { 
        margin: 0 1;    /* Reducimos márgenes */
        height: auto; 
    }
    Horizontal { 
        align: left middle; 
        height: auto; 
        width: 100%;    /* Ocupa todo el ancho disponible */
        margin: 0 1;    /* Reducimos márgenes */
    }
    Vertical { 
        height: auto; 
        width: 100%;    /* Ocupa todo el ancho disponible */
        margin: 0;      /* Eliminamos márgenes */
    }
    #publicaciones { 
        margin-top: 0;  /* Reducimos el margen superior */
        height: auto; 
        width: 100%;    /* Ocupa todo el ancho disponible */
    }
    #usuario_actual { 
        color: white; 
        margin: 0 1;    /* Reducimos márgenes */
    }
    #btn_publicar { 
        background: #F5F5DC !important; 
        color: black !important; 
        width: 8; 
    }
    #btn_lista_usuarios { 
        background: #F5F5DC !important; 
        color: black !important; 
        width: 15; 
    }
    .like-button { 
        background: #F5F5DC; 
        color: black; 
        width: auto; 
        height: 1; 
        padding: 0 1; 
        margin: 0 1; 
    }
    .like-button:hover { 
        background: #FF5555; 
        color: white; 
    }
    .comment-button { 
        background: #F5F5DC; 
        color: black; 
        width: auto; 
        height: 1; 
        padding: 0 1; 
        margin: 0 1; 
    }
    .comment-button:hover { 
        background: #55FF55; 
        color: black; 
    }
    #comment_container { 
        display: none; 
        height: auto; 
        width: 100%;    /* Ocupa todo el ancho disponible */
        margin: 0 1;    /* Reducimos márgenes */
    }
    #comment_input { 
        width: 70%; 
        height: auto; 
    }
    #submit_comment { 
        width: 8; 
        height: auto; 
        background: #F5F5DC !important; 
        color: black !important; 
    }
    #btn_volver { 
        margin: 0 1;    /* Reducimos márgenes */
    }
    .comment-text {
        color: $text-muted;
        width: 60%;     /* Limita el ancho del texto para dejar espacio a los botones */
    }
    .reply-text-1 {
        color: $text-muted;
        width: 60%;
    }
    .reply-text-2 {
        color: $text-muted;
        width: 60%;
    }
    .reply-text-3 {
        color: $text-muted;
        width: 60%;
    }
    .reply-text-4 {
        color: $text-muted;
        width: 60%;
    }
    """

    def __init__(self, usuario, nombre):
        super().__init__()
        self.usuario = usuario
        self.nombre = nombre
        self.post_ids = {}
        self.current_comment_post_id = None
        self.current_comment_path = None
        inicializar_firebase()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static(f"@{self.usuario} ({self.nombre})", id="usuario_actual"),
            Horizontal(
                Button("Ver Lista de Usuarios", id="btn_lista_usuarios"),
                Input(placeholder="¿Qué está pasando?", id="mensaje_input"),
                Button("Scrib", id="btn_publicar")
            ),
            ListView(id="publicaciones"),
            ListView(id="lista_usuarios", classes="hidden"),
            Horizontal(
                Input(placeholder="Escribe un comentario...", id="comment_input"),
                Button("Enviar", id="submit_comment"),
                id="comment_container"
            ),
            Button("Volver al Menú", id="btn_volver", variant="warning")
        )

    def on_mount(self) -> None:
        self.cargar_publicaciones()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_publicar":
            self.crear_publicacion()
        elif event.button.id == "btn_lista_usuarios":
            self.listar_usuarios()
        elif event.button.id == "btn_volver":
            self.exit()
        elif event.button.id == "submit_comment":
            self.enviar_comentario()

    def on_click(self, event: Click) -> None:
        widget = event.control if hasattr(event, 'control') else None
        if widget and widget.id:
            print(f"[DEBUG] Click en widget con ID: {widget.id}")
            if widget.id.startswith("like_") and not widget.id.startswith("comment_like_") and not widget.id.startswith("reply_like_"):
                post_id = widget.id.replace("like_", "")
                self.dar_me_gusta(post_id)
            elif widget.id.startswith("comment_") and not widget.id.startswith("comment_like_") and not widget.id.startswith("comment_reply_"):
                post_id = widget.id.replace("comment_", "")
                self.mostrar_campo_comentario(post_id)
            elif widget.id.startswith("comment_like_"):
                comment_id = widget.id.replace("comment_like_", "")
                self.dar_me_gusta_comentario(comment_id)
            elif widget.id.startswith("comment_reply_"):
                comment_id = widget.id.replace("comment_reply_", "")
                try:
                    post_id, comment_path = comment_id.split("_", 1)
                    print(f"[DEBUG] Intentando responder al comentario con path {comment_path} de la publicación {post_id}")
                    self.mostrar_campo_comentario(post_id, comment_path, is_reply=True)
                except ValueError as e:
                    print(f"[DEBUG] Error al parsear comment_id: {comment_id}, error: {e}")
                    self.notify("Error al intentar responder al comentario.", severity="error")
            elif widget.id.startswith("reply_like_"):
                reply_id = widget.id.replace("reply_like_", "")
                self.dar_me_gusta_respuesta(reply_id)

    def crear_publicacion(self):
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
                    'liked_by': [],
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
        publicaciones = self.query_one("#publicaciones", ListView)
        lista_usuarios = self.query_one("#lista_usuarios", ListView)
        publicaciones.clear()
        self.post_ids.clear()
        try:
            ref = db.reference('publicaciones')
            posts = ref.get()
            if posts:
                for index, (post_id, datos) in enumerate(posts.items()):
                    print(f"[DEBUG] Cargando publicación con post_id: {post_id}")
                    nombre = datos.get('nombre', 'Desconocido')
                    usuario = datos.get('usuario', 'Anon')
                    hora = datos.get('hora', 'Sin fecha')
                    mensaje = datos.get('mensaje', 'Sin mensaje')
                    likes = datos.get('likes', 0)
                    comentarios = datos.get('comentarios', [])
                    
                    scrib_text = f"{nombre} @{usuario} · {hora}\n{mensaje}\n({likes} Me gusta)"
                    scrib = Static(scrib_text)
                    
                    like_button = Static("Me gusta", id=f"like_{post_id}", classes="like-button")
                    comment_button = Static("Comentar", id=f"comment_{post_id}", classes="comment-button")
                    
                    comments_content = []
                    if comentarios:
                        for i, comentario in enumerate(comentarios):
                            comment_path = str(i)
                            comments_content.append(self._render_comment(post_id, comment_path, comentario, usuario))

                    publicaciones.append(ListItem(Vertical(
                        scrib,
                        Horizontal(like_button, comment_button),
                        *comments_content
                    )))
                    self.post_ids[index] = post_id
                
                publicaciones.remove_class("hidden")
                lista_usuarios.add_class("hidden")
            else:
                publicaciones.append(ListItem(Static("No hay scribs aún.")))
            self.query_one("#comment_container").styles.display = "none"
        except Exception as e:
            self.notify(f"Error al cargar publicaciones: {e}", severity="error")

    def _render_comment(self, post_id, comment_path, comentario, usuario, level=1, is_last=True, parent_prefix=""):
        """Renderiza un comentario o respuesta recursivamente con ramas visuales."""
        comment_id = f"{post_id}_{comment_path}"
        comment_text = f"{comentario['autor']} (@{comentario.get('usuario', usuario)}): {comentario['contenido']}"
        comment_likes = comentario.get('likes', 0)
        
        # Construir el prefijo con ramas visuales
        prefix = "└ " if level == 1 else f"{parent_prefix}{'└ ' if is_last else '├ '}"
        if level > 1:
            parent_prefix = f"{parent_prefix}{'  ' if is_last else '│ '}"
        comment_text = f"{prefix}{comment_text}"
        
        # Determinar la clase CSS según el nivel de anidamiento
        css_class = "comment-text" if level == 1 else f"reply-text-{min(level-1, 4)}"
        
        # Crear los botones
        comment_like = Static(f"Me gusta ({comment_likes})", 
                            id=f"{'comment_like' if level == 1 else 'reply_like'}_{comment_id}", 
                            classes="like-button")
        comment_reply = Static("Responder", 
                            id=f"comment_reply_{comment_id}", 
                            classes="comment-button")
        
        # Mostrar el texto y los botones en una sola línea
        comment_line = Horizontal(
            Static(comment_text, classes=css_class),
            comment_like,
            comment_reply
        )
        
        # Cargar respuestas recursivamente
        replies_content = []
        respuestas = comentario.get('respuestas', [])
        if respuestas:
            for j, respuesta in enumerate(respuestas):
                reply_path = f"{comment_path}_{j}"
                is_last_reply = (j == len(respuestas) - 1)
                replies_content.append(self._render_comment(post_id, reply_path, respuesta, usuario, level + 1, is_last_reply, parent_prefix))

        return Vertical(
            comment_line,
            *replies_content
        )

    def dar_me_gusta(self, post_id):
        try:
            ref = db.reference(f'publicaciones/{post_id}')
            post = ref.get()
            if post:
                liked_by = post.get('liked_by', [])
                current_likes = post.get('likes', 0)
                if self.usuario in liked_by:
                    liked_by.remove(self.usuario)
                    ref.update({
                        'likes': current_likes - 1,
                        'liked_by': liked_by
                    })
                    self.notify("Me gusta quitado.", severity="information")
                else:
                    liked_by.append(self.usuario)
                    ref.update({
                        'likes': current_likes + 1,
                        'liked_by': liked_by
                    })
                    self.notify("¡Me gusta registrado!", severity="information")
                self.cargar_publicaciones()
            else:
                self.notify("No se encontró la publicación.", severity="error")
        except Exception as e:
            self.notify(f"Error al dar/quitar Me gusta: {e}", severity="error")

    def dar_me_gusta_comentario(self, comment_id):
        try:
            post_id, comment_idx = comment_id.split("_", 1)
            ref = db.reference(f'publicaciones/{post_id}')
            post = ref.get()
            if post and 'comentarios' in post:
                comentarios = post['comentarios']
                if int(comment_idx) < len(comentarios):
                    comentario = comentarios[int(comment_idx)]
                    liked_by = comentario.get('liked_by', [])
                    current_likes = comentario.get('likes', 0)
                    
                    if self.usuario in liked_by:
                        liked_by.remove(self.usuario)
                        comentarios[int(comment_idx)]['likes'] = current_likes - 1
                    else:
                        liked_by.append(self.usuario)
                        comentarios[int(comment_idx)]['likes'] = current_likes + 1
                    comentarios[int(comment_idx)]['liked_by'] = liked_by
                    
                    ref.update({'comentarios': comentarios})
                    self.notify("¡Like actualizado en comentario!", severity="information")
                    self.cargar_publicaciones()
                else:
                    self.notify("Comentario no encontrado.", severity="error")
            else:
                self.notify("Publicación no encontrada.", severity="error")
        except Exception as e:
            self.notify(f"Error al dar like al comentario: {e}", severity="error")

    def dar_me_gusta_respuesta(self, reply_id):
        try:
            post_id, reply_path = reply_id.split("_", 1)
            ref = db.reference(f'publicaciones/{post_id}')
            post = ref.get()
            if post and 'comentarios' in post:
                comentarios = post['comentarios']
                indices = reply_path.split("_")
                current_level = comentarios
                target_comment = None
                for i, idx in enumerate(indices):
                    idx = int(idx)
                    if idx < len(current_level):
                        if i == len(indices) - 1:
                            target_comment = current_level[idx]
                        else:
                            current_level = current_level[idx].get('respuestas', [])
                    else:
                        self.notify("Respuesta no encontrada.", severity="error")
                        return

                if target_comment:
                    liked_by = target_comment.get('liked_by', [])
                    current_likes = target_comment.get('likes', 0)
                    
                    if self.usuario in liked_by:
                        liked_by.remove(self.usuario)
                        target_comment['likes'] = current_likes - 1
                    else:
                        liked_by.append(self.usuario)
                        target_comment['likes'] = current_likes + 1
                    target_comment['liked_by'] = liked_by
                    
                    current_level = comentarios
                    for i, idx in enumerate(indices[:-1]):
                        idx = int(idx)
                        current_level = current_level[idx]['respuestas']
                    current_level[int(indices[-1])] = target_comment
                    
                    ref.update({'comentarios': comentarios})
                    self.notify("¡Like actualizado en respuesta!", severity="information")
                    self.cargar_publicaciones()
                else:
                    self.notify("Respuesta no encontrada.", severity="error")
            else:
                self.notify("Publicación no encontrada.", severity="error")
        except Exception as e:
            self.notify(f"Error al dar like a la respuesta: {e}", severity="error")

    def mostrar_campo_comentario(self, post_id, comment_path=None, is_reply=False):
        print(f"[DEBUG] Mostrando campo comentario para post_id: {post_id}, comment_path: {comment_path}, is_reply: {is_reply}")
        ref = db.reference(f'publicaciones/{post_id}')
        post = ref.get()
        if not post:
            print(f"[DEBUG] No se encontró la publicación con post_id: {post_id}")
            self.notify("No se encontró la publicación para comentar.", severity="error")
            return

        self.current_comment_post_id = post_id
        self.current_comment_path = comment_path if is_reply else None
        comment_container = self.query_one("#comment_container")
        comment_container.styles.display = "block"
        comment_input = self.query_one("#comment_input")
        comment_input.placeholder = "Escribe una respuesta..." if is_reply else "Escribe un comentario..."
        comment_input.focus()

    def enviar_comentario(self):
        print(f"[DEBUG] Enviando comentario para post_id: {self.current_comment_post_id}, comment_path: {self.current_comment_path}")
        if not self.current_comment_post_id:
            print("[DEBUG] No hay post_id definido para enviar el comentario.")
            self.notify("No se ha seleccionado una publicación para comentar.", severity="error")
            return

        ref = db.reference(f'publicaciones/{self.current_comment_post_id}')
        post = ref.get()
        if not post:
            print(f"[DEBUG] No se encontró la publicación con post_id: {self.current_comment_post_id} al enviar comentario.")
            self.notify("No se encontró la publicación.", severity="error")
            self.current_comment_post_id = None
            self.current_comment_path = None
            return

        comment_input = self.query_one("#comment_input", Input)
        comentario = comment_input.value.strip()
        if comentario:
            try:
                comentarios = post.get('comentarios', [])
                new_comment = {
                    'autor': self.nombre,
                    'usuario': self.usuario,
                    'contenido': comentario,
                    'hora': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'likes': 0,
                    'liked_by': [],
                    'respuestas': []
                }

                if self.current_comment_path is not None:
                    indices = self.current_comment_path.split("_")
                    current_level = comentarios
                    for i, idx in enumerate(indices[:-1]):
                        idx = int(idx)
                        if idx < len(current_level):
                            current_level = current_level[idx].get('respuestas', [])
                        else:
                            self.notify("No se encontró el comentario padre para responder.", severity="error")
                            return
                    idx = int(indices[-1])
                    if idx < len(current_level):
                        if 'respuestas' not in current_level[idx]:
                            current_level[idx]['respuestas'] = []
                        current_level[idx]['respuestas'].append(new_comment)
                        print(f"[DEBUG] Respuesta agregada al path {self.current_comment_path} de la publicación {self.current_comment_post_id}")
                    else:
                        self.notify("Comentario no encontrado para responder.", severity="error")
                        return
                else:
                    comentarios.append(new_comment)
                    print(f"[DEBUG] Comentario directo agregado a la publicación {self.current_comment_post_id}")

                ref.update({'comentarios': comentarios})
                self.notify("Comentario agregado con éxito!", severity="information")
                comment_input.value = ""
                self.query_one("#comment_container").styles.display = "none"
                self.current_comment_post_id = None
                self.current_comment_path = None
                self.cargar_publicaciones()
            except Exception as e:
                print(f"[DEBUG] Error al enviar comentario: {e}")
                self.notify(f"Error al agregar comentario: {e}", severity="error")
        else:
            self.notify("El comentario no puede estar vacío.", severity="error")

# Función para ejecutar el módulo
def ejecutar_gestion_publicacion(usuario, nombre):
    app = GestionPublicacion(usuario, nombre)
    app.run()

if __name__ == "__main__":
    usuario_prueba = "UsuarioPrueba"
    nombre_prueba = "Usuario Prueba"
    print(f"Simulando sesión con @{usuario_prueba} ({nombre_prueba})")
    ejecutar_gestion_publicacion(usuario_prueba, nombre_prueba)