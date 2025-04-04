import firebase_admin
from firebase_admin import credentials, db
import os
import json
import sys

def initialize_firebase():
    # Obtener el directorio donde está firebase_config.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cred_path = os.path.join(current_dir, 'cred.json')
    
    # Verificar si el archivo existe
    if not os.path.exists(cred_path):
        print("[INFO] El archivo 'cred.json' no se encuentra. Creando uno con credenciales predeterminadas...")
        # Credenciales reales de tu proyecto (reemplaza con las tuyas)
        placeholder_data = {
            "type": "service_account",
            "project_id": "scrum-c1f2c",
            "private_key_id": "7325a9886e799faac898e85aabba6bd12b12080d",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCbDIsXblNKPvaX\n8KA9e1orX5H5syRWkCpfJqDRWe1Z7Ocue9BFmjBLnQWy18I5iM8pbL2gDV16kc1b\nP1oidUhmcfLS8adpsobRRiEQ/Z2GhPm0CZ4lw7Jb5QYzIuCEtBm7wPoK0HUwhqXU\nlJ05Gm4hytSusF8zLoClncCEmDEsca008Lr8dcDgGHTbq1z01P19pG0TQ2gZgAZi\nlVGEvfc38qtvL1IOAV6nxrT8fKRxfeHkpgYT+tNU8iODG1VBgQHOsxP8rSHL92au\nVS1OJyfjsFjLa+moZPHVrLGJTWAoc5r0J50bQjxPqpeVAMoq4dtbaWzKIm2UclbZ\nxdVPhmB9AgMBAAECggEAA58Mte9jDUjghDaf3M+/Zg6atN+flFCprK8/nPl3YbJM\nHqR6/iUrxkL/RGi6+z0GxEuV4jcYXSnVR1xOGUqZS6CTBfo+6WkSB7FA9HSinpGx\n2Kf2LvZIeXz6jWyIceZYSNpTp2JXBQXKubxUL7vo9pZrgT5SpY9gfH3CvAC8pUe5\nF4VoyC4VAlk5cxGGWoPHgfbuooKXbLjzc2SDnxMvAThzP/GMYYDuJqRZQD0vBTqI\nl82Lbl+cUItuKpktVXjMlwzOVkwlKI7hwyDdm4lA7HajmmQdsM7S80zU/h+IDXKJ\nPnIEv8CGq6oGOVxzl/UBm0VpWk6jAPqcehqDdhRowQKBgQDR73+1+mvmqcqWVDZu\ntOTp20raKS5qUfZFseXk5ZFeqoYsLYZcaBsTogynTZvMia0h5MN6dMaYnwrb6pNh\n+AkSyOwj6s67MA6S3ffjRell/CMkfYUW63N+vPBA/82AdbwZks1y2LE4Jaw6IdED\nduaVEXEEGWp8QqdMRQB6oj58iwKBgQC9EfT7mWuMiY3nLVCRQOtHTPrsUVjnmDMz\nedV/pSwGbBDEUc4lTgrsGO6y00P6Sh63lLZMFOIpvKLP9BHGBYs2aBuq3ioWb4bE\nUF7zOCcoazFRkUsob+xccRRAUlTq6D/AjBFhRFw09+0Z/Brgua3bNEfqE0jk5V6k\n/4g25fGQFwKBgHJUVx3Y6mhtMYobBKXX2A7PwXz8Dm4SgudD0eqNZ1TB01490L2E\naLKRfwiiCGYk2Gfr+NU4wWseukA4CNnCxdY4G/oXh0yECHvNbJGWYlyLKuxVe2SX\nB4gPB1yustDxzWW0ADU6c5EbWycxgW28lCi8nerYmJhhiFDOB0vCDfuvAoGAKZYc\ni4aoWEYdNz8JXJmp5onxGy+dXXtlr6nZovTipRr56SSRMjVjQ6EMR7seVZwd+4Uz\nP7LMOB/ss87cZfDsOPBXPZMWMM8hFmcTK24rdsF1HJrXrDJKC983dBpn4S9qbmCg\npgNSQLhTp4aDJvDQY8mxE7RgMTCeS66E+IZFRssCgYEAw7cn+Ii9MQuN0+m/FG7G\n6nZVZQoMTOl18ac2Ma8dpvtUB6kPXvsBSFc+V2HFP/po9Rn3d1McGXrvdDtZbodb\n6qRaeFRI/To8ZJdjjakqZzpg4blE87ZCVcRIEOYWcCmA50AhLI1jkIdKmDu1NMTb\nbV8C/li33jKkDgJt1t2MaAY=\n-----END PRIVATE KEY-----\n",
            "client_email": "firebase-adminsdk-fbsvc@scrum-c1f2c.iam.gserviceaccount.com",
            "client_id": "102303364724447533678",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40scrum-c1f2c.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
        }
        with open(cred_path, 'w') as f:
            json.dump(placeholder_data, f, indent=4)
        print(f"[INFO] Archivo 'cred.json' creado en {cred_path} con credenciales predeterminadas.")

    # Cargar las credenciales desde el archivo
    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://scrum-c1f2c-default-rtdb.firebaseio.com/'  # Reemplaza con tu URL real
        })
        print("[Firebase] Conexión inicializada con éxito")
    except ValueError as e:
        print(f"[ERROR] El archivo 'cred.json' no es válido: {e}")
        print("[INFO] Verifica que las credenciales sean correctas.")
        sys.exit(1)

# Inicializar Firebase al importar el módulo
initialize_firebase()