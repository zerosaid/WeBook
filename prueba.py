import firebase_admin
from firebase_admin import credentials, firestore, auth
import logging
import os
import datetime

# Configuración de logs
LOG_FILE = "app.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Inicialización de Firebase
CRED_PATH = "/home/camper/Escritorio/WeBook/WeBook/cred.json"  # Cambiar por la ruta real
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CRED_PATH
cred = credentials.Certificate(CRED_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Función para registrar logs
def registrar_log(mensaje):
    logging.info(mensaje)
    print(mensaje)

# Manejo de usuarios en Firebase Authentication
def registrar_usuario(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        registrar_log(f"Usuario creado: {user.uid}")
        return user.uid
    except Exception as e:
        registrar_log(f"Error al registrar usuario: {e}")
        return None

def eliminar_usuario(uid):
    try:
        auth.delete_user(uid)
        registrar_log(f"Usuario {uid} eliminado correctamente.")
    except Exception as e:
        registrar_log(f"Error al eliminar usuario: {e}")

# Funciones CRUD para Firestore
def agregar_documento(coleccion, datos):
    try:
        ref = db.collection(coleccion).add(datos)
        registrar_log(f"Documento agregado en {coleccion}: {ref}")
    except Exception as e:
        registrar_log(f"Error al agregar documento: {e}")

def obtener_documentos(coleccion):
    try:
        docs = db.collection(coleccion).stream()
        for doc in docs:
            registrar_log(f"{doc.id} => {doc.to_dict()}")
    except Exception as e:
        registrar_log(f"Error al obtener documentos: {e}")

def actualizar_documento(coleccion, documento_id, nuevos_datos):
    try:
        db.collection(coleccion).document(documento_id).update(nuevos_datos)
        registrar_log(f"Documento {documento_id} actualizado en {coleccion}.")
    except Exception as e:
        registrar_log(f"Error al actualizar documento: {e}")

def eliminar_documento(coleccion, documento_id):
    try:
        db.collection(coleccion).document(documento_id).delete()
        registrar_log(f"Documento {documento_id} eliminado de {coleccion}.")
    except Exception as e:
        registrar_log(f"Error al eliminar documento: {e}")

# Interfaz de usuario (CLI)
def menu():
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Registrar usuario")
        print("2. Eliminar usuario")
        print("3. Agregar documento")
        print("4. Obtener documentos")
        print("5. Actualizar documento")
        print("6. Eliminar documento")
        print("7. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            email = input("Ingrese el correo del usuario: ")
            password = input("Ingrese la contraseña: ")
            registrar_usuario(email, password)
        elif opcion == "2":
            uid = input("Ingrese el UID del usuario: ")
            eliminar_usuario(uid)
        elif opcion == "3":
            coleccion = input("Ingrese la colección: ")
            clave = input("Ingrese el campo: ")
            valor = input("Ingrese el valor: ")
            agregar_documento(coleccion, {clave: valor})
        elif opcion == "4":
            coleccion = input("Ingrese la colección: ")
            obtener_documentos(coleccion)
        elif opcion == "5":
            coleccion = input("Ingrese la colección: ")
            documento_id = input("Ingrese el ID del documento: ")
            clave = input("Ingrese el campo a actualizar: ")
            valor = input("Ingrese el nuevo valor: ")
            actualizar_documento(coleccion, documento_id, {clave: valor})
        elif opcion == "6":
            coleccion = input("Ingrese la colección: ")
            documento_id = input("Ingrese el ID del documento: ")
            eliminar_documento(coleccion, documento_id)
        elif opcion == "7":
            print("Saliendo...")
            break
        else:
            print("Opción no válida, intente nuevamente.")

if __name__ == "__main__":
    menu()
