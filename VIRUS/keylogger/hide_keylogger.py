from stegano import lsb

with open('tu_ejecutable.exe', 'rb') as f:
    executable_data = f.read()

secret_image = lsb.hide('imagen.jpg', executable_data)
secret_image.save('imagen_con_ejecutable.png')