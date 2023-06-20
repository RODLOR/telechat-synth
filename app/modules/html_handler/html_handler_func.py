from bs4 import BeautifulSoup
import requests
import time

def clear_html_to_text(html_element):
    element = BeautifulSoup(html_element, 'html.parser')
    texto_limpio = element.get_text()
    return texto_limpio

def clear_html_to_img(html_element, img_class):
    element = BeautifulSoup(html_element, 'html.parser')
    # Extraer las imágenes
    if element.find(class_=img_class):        
        imagenes = element.find_all(class_=img_class)
        for imagen in enumerate(imagenes):
            src = imagen['src']
            alt = imagen.get('alt', '')
            nombre_archivo = f"./assets/img/{alt}.jpg"
            # Descargar la imagen
            time.sleep(5)
            response = requests.get(src)
            # Guardar la imagen
            with open(nombre_archivo, 'wb') as f:
                f.write(response.content)
                f.close()
    else: return None
