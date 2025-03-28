from base_d import FirebaseDB
from datetime import datetime
from encriptacion import *
path ="cred.json"
url ="https://scrum-c1f2c-default-rtdb.firebaseio.com/"
fb_db = FirebaseDB(path,url)
def vericacion_users(usuario, password):
    # Read data from the database
    result = fb_db.read_record(f'/usuarios/{usuario}')
    print (result)
    print (password)

    return result and check_password_static(password, result['password'])

def save_usuarios(email, new_usuario, new_password):
    # Write data to the database
    ref = fb_db.read_record(f'/usuarios{new_usuario}')
    if not ref:
        hashed_password = hash_password_static(new_password)
        # Write data to the specified path in the Realtime Database
        data_to_write = {
            "email":email,
            'usuario': new_usuario,
            'password': hashed_password,
            'fecha_creacion': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        fb_db.write_record(f'/usuarios/{email.split("@")[0]}', data_to_write)
        return True

#print(vericacion_users('jfleong6',"1234"))
"""
# Write data to the database
data_to_write = {
'name': 'jj',
'age': 27,
'email': 'jj@gmail.com'
}
fb_db.write_record('/users/jj', data_to_write)

# Read data from the database
result = fb_db.read_record('/users/toni')
print("Read Data:", result)

# Update data in the database
data_to_update = {
'age': 31
}
fb_db.update_record('/users/toni', data_to_update)

# Delete data from the database
fb_db.delete_record('/users/john_doe')

# Delete data from the database
fb_db.delete_record('/users/toni')

# to save a record with an unique id
ref = db.reference('users')
new_email_ref = ref.push()
new_email_ref.set({
    'name': 'Juan',
    'email': 'Juan@hotmail.com'
})

"""