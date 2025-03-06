import qrcode
from PIL import Image
import os
import requests
from io import BytesIO

logo_url = r'https://raw.githubusercontent.com/juliancastillo-udea/Intro_SBA_ASOCIO_20250311/refs/heads/main/images/ICON_ASOCIO.png'

# Crear instancia del código QR
qr = qrcode.QRCode(
    version=1,  
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # Nivel de corrección de errores
    box_size=10,  # Tamaño de cada caja del QR
    border=4,  # Tamaño del borde del QR
)
qr.add_data('https://github.com/juliancastillo-udea/Intro_SBA_ASOCIO_20250311')  # Ruta del contenido del taller de agentes
qr.make(fit=True)  # Ajustar el tamaño del QR 

# Crear la imagen del código QR
qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')  # Crear la imagen del QR en negro y blanco

# Descargar el icono de ASOCIO
response = requests.get(logo_url)
logo = Image.open(BytesIO(response.content))  # Usando IO descargamos el contenido

# Calcular el tamaño del logo
logo_size = 150  # Tamaño deseado del logo para garantizar que se vea
logo.thumbnail((logo_size, logo_size))  # Redimensionar el logo manteniendo la relación de aspecto

# Calcular la posición para centrar el logo
qr_width, qr_height = qr_img.size  # Obtener el tamaño del QR
logo_width, logo_height = logo.size  # Obtener el tamaño del logo
x = (qr_width - logo_width) // 2  # Calcular la posición X para centrar el logo
y = (qr_height - logo_height) // 2  # Calcular la posición Y para centrar el logo

# Pegar el logo en el centro del código QR
qr_img.paste(logo, (x, y), logo)  # Pegar el logo en la imagen del QR

# Guardar la imagen final
qr_img.save('QR_Agentes_ASOCIO.png')  # Guardar la imagen del QR con el logo