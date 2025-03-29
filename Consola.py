from requests import post
from textual.app import App
from textual.widgets import Button, Input, Static, Container
from textual.reactive import Reactive

class CommentApp(App):
    posts = Reactive([])

    def on_mount(self):
        # Crear algunas publicaciones de ejemplo
        self.posts.append(post("¡Hola, mundo!"))
        self.posts.append(post("Este es un segundo post."))
        self.show_posts()

    def show_posts(self):
        for post in self.posts:
            self.add_post_widget(post)

    def add_post_widget(self, post):
        # Aquí se agregarán los widgets para cada publicación
        pass

    def add_comment(self, post, input_field):
        # Aquí se manejará la lógica para agregar un comentario
        pass

    def refresh(self):
        # Aquí se actualizará la vista
        pass

if __name__ == "__main__":
    CommentApp.run()