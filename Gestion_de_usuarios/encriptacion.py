import hashlib

def hash_password_static(password: str) -> str:
    """Genera un hash SHA-256 estático (siempre el mismo para la misma entrada)."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def check_password_static(password: str, hashed_password: str) -> bool:
    """Verifica si el hash de la contraseña coincide con el almacenado."""
    return hash_password_static(password) == hashed_password

'''
password = "1234"
hashed_password = hash_password_static(password)  # Siempre el mismo hash para la misma contraseña

print(f"Contraseña original: {password}")
print(f"Hash generado: {hashed_password}")

# Verificar después
input_password = "1234"
is_correct = check_password_static(input_password, hashed_password)

print(f"¿La contraseña es correcta? {is_correct}")  # True


'''