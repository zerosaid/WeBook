from firebase_admin import db
from datetime import datetime
from base_d import Post, Comment
from typing import List, Dict, Any, Optional

class PostManager:
    @staticmethod
    def create_post(nombre: str, usuario: str, mensaje: str) -> str:
        try:
            ref = db.reference('publicaciones')
            nueva_pub = ref.push()
            hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            post_data = {
                'nombre': nombre,
                'usuario': usuario,
                'hora': hora,
                'mensaje': mensaje,
                'likes': 0,
                'liked_by': [],
                'comentarios': []
            }
            nueva_pub.set(post_data)
            post_id = nueva_pub.key
            print(f"[DEBUG] Post creado con ID: {post_id}, datos: {post_data}")
            saved_post = ref.child(post_id).get()
            print(f"[DEBUG] Verificación post guardado con ID: {post_id}, resultado: {saved_post}")
            if not saved_post:
                raise Exception(f"El post con ID {post_id} no se guardó correctamente en Firebase")
            return post_id
        except Exception as e:
            print(f"[DEBUG] Error al crear publicación: {e}")
            raise Exception(f"Error al crear publicación: {e}")

    @staticmethod
    def get_all_posts() -> List[Post]:
        try:
            ref = db.reference('publicaciones')
            posts = ref.get()
            print(f"[DEBUG] Obteniendo todas las publicaciones, resultado: {posts}")
            if not posts:
                print("[DEBUG] No hay publicaciones en Firebase")
                return []
            return [Post.from_dict(post_id, data) for post_id, data in posts.items()]
        except Exception as e:
            print(f"[DEBUG] Error al cargar publicaciones: {e}")
            raise Exception(f"Error al cargar publicaciones: {e}")

    @staticmethod
    def get_post(post_id: str) -> Optional[Post]:
        try:
            ref = db.reference(f'publicaciones/{post_id}')
            post = ref.get()
            print(f"[DEBUG] Obteniendo post con post_id: {post_id}, resultado: {post}")
            if not post:
                print(f"[DEBUG] No se encontró post con post_id: {post_id} en Firebase")
                return None
            return Post.from_dict(post_id, post)
        except Exception as e:
            print(f"[DEBUG] Error al obtener publicación {post_id}: {e}")
            raise Exception(f"Error al obtener publicación {post_id}: {e}")

    @staticmethod
    def like_post(post_id: str, usuario: str) -> None:
        try:
            ref = db.reference(f'publicaciones/{post_id}')
            post = ref.get()
            if not post:
                raise Exception("Publicación no encontrada")
            liked_by = post.get('liked_by', [])
            current_likes = post.get('likes', 0)
            if usuario in liked_by:
                liked_by.remove(usuario)
                ref.update({'likes': current_likes - 1, 'liked_by': liked_by})
            else:
                liked_by.append(usuario)
                ref.update({'likes': current_likes + 1, 'liked_by': liked_by})
        except Exception as e:
            raise Exception(f"Error al dar/quitar Me gusta: {e}")

    @staticmethod
    def like_comment(post_id: str, comment_path: List[int], usuario: str) -> None:
        try:
            ref = db.reference(f'publicaciones/{post_id}')
            post = ref.get()
            if not post or 'comentarios' not in post:
                raise Exception("Publicación o comentario no encontrado")
            comentarios = post['comentarios']
            current_level = comentarios
            for idx in comment_path[:-1]:
                current_level = current_level[idx]['respuestas']
            comentario = current_level[comment_path[-1]]
            liked_by = comentario.get('liked_by', [])
            current_likes = comentario.get('likes', 0)
            if usuario in liked_by:
                liked_by.remove(usuario)
                comentario['likes'] = current_likes - 1
            else:
                liked_by.append(usuario)
                comentario['likes'] = current_likes + 1
            comentario['liked_by'] = liked_by
            current_level[comment_path[-1]] = comentario
            ref.update({'comentarios': comentarios})
        except Exception as e:
            raise Exception(f"Error al dar like al comentario: {e}")

    @staticmethod
    def add_comment(post_id: str, comment: Comment, comment_path: List[int] = None) -> None:
        try:
            ref = db.reference(f'publicaciones/{post_id}')
            post = ref.get()
            if not post:
                raise Exception("Publicación no encontrada")
            comentarios = post.get('comentarios', [])
            if not comment_path:
                comentarios.append(comment.to_dict())
            else:
                current_level = comentarios
                for idx in comment_path[:-1]:
                    current_level = current_level[idx]['respuestas']
                last_idx = comment_path[-1]
                current_level[last_idx].setdefault('respuestas', []).append(comment.to_dict())
            ref.update({'comentarios': comentarios})
        except Exception as e:
            raise Exception(f"Error al agregar comentario: {e}")