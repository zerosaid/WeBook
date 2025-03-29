from textual.app import Screen, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Input, Button, Header, Static, ListView, ListItem
from textual.events import Click
from post_manager import PostManager
from base_d import Post, Comment
from datetime import datetime
from conexion import listar_usuarios

class PublicationScreen(Screen):
    CSS = """
    Static { 
        width: 100%; 
        padding: 0 1; 
        margin: 0; 
        background: transparent; 
        color: white;
    }
    ListView { 
        height: auto; 
        max-height: 15; 
        border: solid white; 
        padding: 0 1; 
        background: transparent; 
    }
    ListItem { 
        height: auto; 
        padding: 0 1; 
        margin: 0; 
        background: transparent; 
    }
    Input { 
        margin: 0 1; 
        width: 50%; 
        height: auto; 
    }
    Button { 
        margin: 0 1; 
        height: auto; 
    }
    Horizontal { 
        align: left middle; 
        height: auto; 
        margin: 0 1; 
    }
    Vertical { 
        height: auto; 
        margin: 0; 
    }
    #publicaciones { 
        margin-top: 0; 
        height: auto; 
    }
    #usuario_actual { 
        color: white; 
        margin: 0 1; 
    }
    #btn_publicar { 
        background: #F5F5DC !important; 
        color: black !important; 
        width: 8; 
    }
    #btn_buscar_usuario { 
        background: #F5F5DC !important; 
        color: black !important; 
        width: 15; 
    }
    .like-button, .comment-button { 
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
    .comment-button:hover { 
        background: #55FF55; 
        color: black; 
    }
    #comment_container { 
        display: none; 
        height: auto; 
        margin: 0 1; 
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
        margin: 0 1; 
    }
    .comment-text, .reply-text-1, .reply-text-2, .reply-text-3, .reply-text-4 { 
        color: $text-muted; 
        padding-left: 2; 
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
        self.post_manager = PostManager()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static(f"@{self.usuario} ({self.nombre})", id="usuario_actual"),
            Horizontal(
                Input(placeholder="¿Qué está pasando?", id="mensaje_input"),
                Button("Scrib", id="btn_publicar")
            ),
            ListView(id="publicaciones"),
            Horizontal(
                Input(placeholder="Escribe un comentario...", id="comment_input"),
                Button("Enviar", id="submit_comment"),
                id="comment_container"
            ),
            Horizontal(
                Input(placeholder="Buscar usuario...", id="search_input"),
                Button("Buscar", id="btn_buscar_usuario")
            ),
            Button("Cerrar Sesión", id="btn_volver", variant="warning")
        )

    def on_mount(self) -> None:
        self.cargar_publicaciones()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_publicar":
            self.crear_publicacion()
        elif event.button.id == "btn_buscar_usuario":
            self.buscar_usuario()
        elif event.button.id == "btn_volver":
            from login_app import LoginScreen
            self.app.switch_screen(LoginScreen())
        elif event.button.id == "submit_comment":
            self.enviar_comentario()

    def on_click(self, event: Click) -> None:
        widget = event.control if hasattr(event, 'control') else None
        if widget and widget.id:
            if widget.id.startswith("like_") and not widget.id.startswith("comment_like_"):
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
                    post_id, comment_path_str = comment_id.split("_", 1)
                    comment_path = [int(i) for i in comment_path_str.split("_")]
                    self.mostrar_campo_comentario(post_id, comment_path, is_reply=True)
                except ValueError as e:
                    self.notify(f"Error al parsear comment_id: {comment_id}, error: {e}", severity="error")

    def crear_publicacion(self):
        mensaje_input = self.query_one("#mensaje_input", Input)
        mensaje = mensaje_input.value.strip()
        if mensaje:
            try:
                post_id = self.post_manager.create_post(self.nombre, self.usuario, mensaje)
                self.notify("Scrib publicado con éxito!", severity="information")
                mensaje_input.value = ""
                self.cargar_publicaciones()
            except Exception as e:
                self.notify(f"Error al crear publicación: {e}", severity="error")
        else:
            self.notify("El scrib no puede estar vacío.", severity="error")

    def buscar_usuario(self):
        search_input = self.query_one("#search_input", Input)
        usuario_buscado = search_input.value.strip()
        if usuario_buscado:
            try:
                usuarios = listar_usuarios()
                if usuarios is None:
                    self.notify("No hay usuarios registrados en la base de datos.", severity="warning")
                    return
                target_usuario = None
                for usuario, data in usuarios.items():
                    if usuario == usuario_buscado or data.get('email') == usuario_buscado:
                        target_usuario = usuario
                        break
                if target_usuario:
                    self.app.switch_screen(UserProfileScreen(self.usuario, self.nombre, target_usuario))
                else:
                    self.notify(f"No se encontró al usuario @{usuario_buscado}.", severity="warning")
            except Exception as e:
                self.notify(f"Error al buscar usuario: {e}", severity="error")
        else:
            self.notify("Por favor, ingresa un nombre de usuario.", severity="error")

    def cargar_publicaciones(self):
        publicaciones = self.query_one("#publicaciones", ListView)
        publicaciones.clear()
        self.post_ids.clear()
        try:
            posts = self.post_manager.get_all_posts()
            if posts:
                for index, post in enumerate(posts):
                    scrib_text = f"{post.nombre} @{post.usuario} · {post.hora}\n{post.mensaje}\n({post.likes} Me gusta)"
                    scrib = Static(scrib_text)
                    like_button = Static("Me gusta", id=f"like_{post.id}", classes="like-button")
                    comment_button = Static("Comentar", id=f"comment_{post.id}", classes="comment-button")
                    comments_content = []
                    if post.comentarios:
                        self._render_comments(post.comentarios, comments_content, post.id, level=0)
                    publicaciones.append(ListItem(Vertical(
                        scrib,
                        Horizontal(like_button, comment_button),
                        *comments_content
                    )))
                    self.post_ids[index] = post.id
            else:
                publicaciones.append(ListItem(Static("No hay scribs aún.")))
            self.query_one("#comment_container").styles.display = "none"
        except Exception as e:
            self.notify(f"Error al cargar publicaciones: {e}", severity="error")

    def _render_comments(self, comentarios, content_list, post_id, level=0, path=None):
        if path is None:
            path = []
        indent = "  " * level
        for i, comentario in enumerate(comentarios):
            current_path = path + [i]
            comment_id = f"{post_id}_{'_'.join(map(str, current_path))}"
            comment_text = f"{indent}- {comentario.autor} (@{comentario.usuario}): {comentario.contenido}"
            comment_likes = comentario.likes
            css_class = "comment-text" if level == 0 else f"reply-text-{min(level, 4)}"
            comment_like = Static(f"Me gusta ({comment_likes})", id=f"comment_like_{comment_id}", classes="like-button")
            comment_reply = Static("Responder", id=f"comment_reply_{comment_id}", classes="comment-button")
            content_list.append(Vertical(
                Static(comment_text, classes=css_class),
                Horizontal(comment_like, comment_reply)
            ))
            if comentario.respuestas:
                self._render_comments(comentario.respuestas, content_list, post_id, level + 1, current_path)

    def dar_me_gusta(self, post_id):
        try:
            self.post_manager.like_post(post_id, self.usuario)
            self.notify("¡Me gusta actualizado!", severity="information")
            self.cargar_publicaciones()
        except Exception as e:
            self.notify(f"Error al dar/quitar Me gusta: {e}", severity="error")

    def dar_me_gusta_comentario(self, comment_id):
        try:
            parts = comment_id.split("_")
            post_id = parts[0]
            comment_path = [int(idx) for idx in parts[1:]]
            self.post_manager.like_comment(post_id, comment_path, self.usuario)
            self.notify("¡Like actualizado en comentario!", severity="information")
            self.cargar_publicaciones()
        except Exception as e:
            self.notify(f"Error al dar like al comentario: {e}", severity="error")

    def mostrar_campo_comentario(self, post_id, comment_path=None, is_reply=False):
        post = self.post_manager.get_post(post_id)
        if not post:
            self.notify("No se encontró la publicación para comentar.", severity="error")
            return
        self.current_comment_post_id = post_id
        self.current_comment_path = comment_path if is_reply else None
        try:
            comment_container = self.query_one("#comment_container")
            comment_container.styles.display = "block"
            comment_input = self.query_one("#comment_input")
            comment_input.placeholder = "Escribe una respuesta..." if is_reply else "Escribe un comentario..."
            comment_input.focus()
        except Exception as e:
            self.notify(f"Error al mostrar el campo de comentario: {e}", severity="error")

    def enviar_comentario(self):
        if not self.current_comment_post_id:
            self.notify("No se ha seleccionado una publicación para comentar.", severity="error")
            return
        post = self.post_manager.get_post(self.current_comment_post_id)
        if not post:
            self.notify("No se encontró la publicación.", severity="error")
            self.current_comment_post_id = None
            self.current_comment_path = None
            return
        comment_input = self.query_one("#comment_input", Input)
        comentario = comment_input.value.strip()
        if comentario:
            try:
                new_comment = Comment(
                    autor=self.nombre,
                    usuario=self.usuario,
                    contenido=comentario,
                    hora=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    likes=0,
                    liked_by=[],
                    respuestas=[]
                )
                self.post_manager.add_comment(self.current_comment_post_id, new_comment, self.current_comment_path or [])
                self.notify("Comentario agregado con éxito!", severity="information")
                comment_input.value = ""
                self.query_one("#comment_container").styles.display = "none"
                self.current_comment_post_id = None
                self.current_comment_path = None
                self.cargar_publicaciones()
            except Exception as e:
                self.notify(f"Error al agregar comentario: {e}", severity="error")
        else:
            self.notify("El comentario no puede estar vacío.", severity="error")

class UserProfileScreen(Screen):
    CSS = """
    Static { 
        width: 100%; 
        padding: 0 1; 
        margin: 0; 
        background: transparent; 
        color: white;
    }
    ListView { 
        height: auto; 
        max-height: 15; 
        border: solid white; 
        padding: 0 1; 
        background: transparent; 
    }
    ListItem { 
        height: auto; 
        padding: 0 1; 
        margin: 0; 
        background: transparent; 
    }
    Button { 
        margin: 0 1; 
        height: auto; 
    }
    Vertical { 
        height: auto; 
        margin: 0; 
    }
    #profile_info { 
        color: white; 
        margin: 0 1; 
    }
    #posts, #comments, #liked { 
        margin-top: 0; 
        height: auto; 
    }
    #btn_volver { 
        margin: 0 1; 
    }
    .comment-text {
        color: $text-muted;
        padding-left: 2;
    }
    """

    def __init__(self, current_usuario, current_nombre, target_usuario):
        super().__init__()
        self.current_usuario = current_usuario
        self.current_nombre = current_nombre
        self.target_usuario = target_usuario
        self.post_manager = PostManager()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static(f"Perfil de @{self.target_usuario}", id="profile_info"),
            ListView(id="posts"),
            ListView(id="comments"),
            ListView(id="liked"),
            Button("Volver", id="btn_volver", variant="warning")
        )

    def on_mount(self) -> None:
        self.cargar_perfil()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_volver":
            self.app.switch_screen(PublicationScreen(self.current_usuario, self.current_nombre))

    def cargar_perfil(self):
        posts_list = self.query_one("#posts", ListView)
        comments_list = self.query_one("#comments", ListView)
        liked_list = self.query_one("#liked", ListView)
        posts_list.clear()
        comments_list.clear()
        liked_list.clear()

        try:
            posts = self.post_manager.get_all_posts()

            user_posts = [post for post in posts if post.usuario == self.target_usuario]
            if user_posts:
                posts_list.append(ListItem(Static("Publicaciones:")))
                for post in user_posts:
                    scrib_text = f"{post.nombre} @{self.target_usuario} · {post.hora}\n{post.mensaje}\n({post.likes} Me gusta)"
                    posts_list.append(ListItem(Static(scrib_text)))
            else:
                posts_list.append(ListItem(Static("No hay publicaciones.")))

            all_comments = []
            def collect_comments(comentarios, path=None):
                if path is None:
                    path = []
                for i, comentario in enumerate(comentarios):
                    current_path = path + [i]
                    if comentario.usuario == self.target_usuario:
                        all_comments.append((current_path, comentario))
                    if comentario.respuestas:
                        collect_comments(comentario.respuestas, current_path)

            for post in posts:
                collect_comments(post.comentarios)

            if all_comments:
                comments_list.append(ListItem(Static("Comentarios:")))
                for path, comentario in all_comments:
                    indent = "  " * len(path)
                    comment_text = f"{indent}- {comentario.autor} (@{self.target_usuario}) · {comentario.hora}\n{indent}  {comentario.contenido}\n{indent}  ({comentario.likes} Me gusta)"
                    comments_list.append(ListItem(Static(comment_text, classes="comment-text")))
            else:
                comments_list.append(ListItem(Static("No hay comentarios.")))

            liked_items = []
            def collect_liked_comments(comentarios, parent_text, level=0):
                indent = "  " * level
                for i, comentario in enumerate(comentarios):
                    if self.target_usuario in comentario.liked_by:
                        liked_items.append(f"{indent}Comentario en {parent_text}: {comentario.autor} (@{comentario.usuario}) · {comentario.hora}\n{indent}  {comentario.contenido}\n{indent}  ({comentario.likes} Me gusta)")
                    if comentario.respuestas:
                        collect_liked_comments(comentario.respuestas, parent_text, level + 1)

            for post in posts:
                if self.target_usuario in post.liked_by:
                    liked_items.append(f"Publicación: {post.nombre} @{post.usuario} · {post.hora}\n{post.mensaje}\n({post.likes} Me gusta)")
                if post.comentarios:
                    parent_text = f"{post.nombre} @{post.usuario}"
                    collect_liked_comments(post.comentarios, parent_text)

            if liked_items:
                liked_list.append(ListItem(Static("Me gusta:")))
                for item in liked_items:
                    liked_list.append(ListItem(Static(item)))
            else:
                liked_list.append(ListItem(Static("No ha dado Me gusta a nada.")))

        except Exception as e:
            self.notify(f"Error al cargar perfil: {e}", severity="error")