from bs4 import BeautifulSoup
import requests

from .rut import rut_to_dict

def scrap_html(url):
    request = requests.get(url)
    return BeautifulSoup(request.text, 'html.parser')


def create_data_for_login(rut, password):
    data = rut_to_dict(rut)

    return {
        'rut': data["rut"],
        'dv': data["dv"],
        'referencia': 'https://misiir.sii.cl/cgi_misii/siihome.cgi',
        '411': '',
        'rutcntr': data["rutcntr"],
        'clave': password,
    }
    
def login_to_sii(rut, password):
    session_requests = requests.Session()

    headers = {
        'Origin': 'https://zeusr.sii.cl',
        'Referer': 'https://zeusr.sii.cl//AUT2000/InicioAutenticacion/IngresoRutClave.html?https://misiir.sii.cl/cgi_misii/siihome.cgi',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

    data = create_data_for_login(rut, password)
    response = session_requests.post('https://zeusr.sii.cl/cgi_AUT2000/CAutInicio.cgi', headers, data)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    if soup.find(id="auth_bottom"):
        print("Login unsuccessful")
        return False
    print("Login successful")
    
    return session_requests

def connect_to_page(url, session):
    return session.get(url)


# python manage.py shell
# from core.utils import *
# response_login = login_to_sii('782413708', 'union2')
# Login successful
# resp = connect_to_page('https://www.sii.cl/servicios_online/', response_login)
# soup = BeautifulSoup(resp.text, 'html.parser')
# title = soup.find('h1')
# title