# base_d.py
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any

@dataclass
class User:
    email: str
    username: str
    password: str

@dataclass
class Comment:
    autor: str
    usuario: str
    contenido: str
    hora: str
    likes: int
    liked_by: List[str]
    respuestas: List['Comment']

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Comment':
        return Comment(
            autor=data.get('autor', 'Desconocido'),
            usuario=data.get('usuario', 'Anon'),
            contenido=data.get('contenido', 'Sin contenido'),
            hora=data.get('hora', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            likes=data.get('likes', 0),
            liked_by=data.get('liked_by', []),
            respuestas=[Comment.from_dict(respuesta) for respuesta in data.get('respuestas', [])]
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'autor': self.autor,
            'usuario': self.usuario,
            'contenido': self.contenido,
            'hora': self.hora,
            'likes': self.likes,
            'liked_by': self.liked_by,
            'respuestas': [respuesta.to_dict() for respuesta in self.respuestas]
        }

@dataclass
class Post:
    id: str
    nombre: str
    usuario: str
    hora: str
    mensaje: str
    likes: int
    liked_by: List[str]
    comentarios: List[Comment]

    @staticmethod
    def from_dict(post_id: str, data: Dict[str, Any]) -> 'Post':
        return Post(
            id=post_id,
            nombre=data.get('nombre', 'Desconocido'),
            usuario=data.get('usuario', 'Anon'),
            hora=data.get('hora', 'Sin fecha'),
            mensaje=data.get('mensaje', 'Sin mensaje'),
            likes=data.get('likes', 0),
            liked_by=data.get('liked_by', []),
            comentarios=[Comment.from_dict(comment) for comment in data.get('comentarios', [])]
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'nombre': self.nombre,
            'usuario': self.usuario,
            'hora': self.hora,
            'mensaje': self.mensaje,
            'likes': self.likes,
            'liked_by': self.liked_by,
            'comentarios': [comment.to_dict() for comment in self.comentarios]
        }