from cryptography.fernet import Fernet

def gen_key():
    key = Fernet.generate_key()
    with open('pass.key', 'wb') as file:
        file.write(key)
        
def load_key():
    return open('pass.key', 'rb').read()

gen_key()

key = load_key()

password = b'dsadxcsfgjpivbnjo'

file = open('pass.enc', 'wb')

clave = Fernet(key)
pass_enc =clave.encrypt(password)
file.write(pass_enc)

file.close

