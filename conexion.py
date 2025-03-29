import datetime
from firebase_admin import db

def vericacion_users(username: str, password: str) -> bool:
    try:
        ref = db.reference('usuarios')
        users = ref.get()
        print(f"[DEBUG] Datos de usuarios obtenidos: {users}")
        if not users:
            print("[DEBUG] No hay usuarios en la base de datos")
            return False
        if username in users:
            stored_password = users[username].get('password')
            print(f"[DEBUG] Contraseña almacenada para {username}: {stored_password}")
            print(f"[DEBUG] Contraseña ingresada: {password}")
            return stored_password == password
        print(f"[DEBUG] No se encontró el usuario: {username}")
        return False
    except Exception as e:
        print(f"[Error] Verificación de usuario fallida: {e}")
        return False

def save_usuarios(email: str, name: str, username: str, password: str) -> bool:
    try:
        ref = db.reference('usuarios')
        users = ref.get()
        print(f"[DEBUG] Datos obtenidos de Firebase: {users}")
        if users is None:
            users = {}
            print("[DEBUG] Base de datos vacía, inicializando users como {}")
        # Verificar si el username o email ya están registrados
        for existing_usuario, data in users.items():
            if existing_usuario == username or data.get('email') == email:
                print(f"[DEBUG] Conflicto: username {username} o email {email} ya existe")
                return False
        # Guardar el usuario con el username como clave
        ref.child(username).set({
            'email': email,
            'name': name,
            'username': username,
            'password': password,
            'fecha_creacion': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        print(f"[DEBUG] Usuario {username} registrado con éxito")
        return True
    except Exception as e:
        print(f"[Error] No se pudo guardar el usuario: {e}")
        return False

def listar_usuarios() -> dict:
    try:
        ref = db.reference('usuarios')
        users = ref.get()
        print(f"[DEBUG] Usuarios listados: {users}")
        return users or {}
    except Exception as e:
        print(f"[Error] No se pudo listar usuarios: {e}")
        return {}