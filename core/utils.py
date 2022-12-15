from bs4 import BeautifulSoup
import requests
from .rut import rut_to_dict

def scrap_html(request):
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
        'Upgrade-Insecure-Requests': '1'
    }

    data = create_data_for_login(rut, password)
    response = session_requests.post('https://zeusr.sii.cl/cgi_AUT2000/CAutInicio.cgi', headers=headers, data=data)
    
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
# resp = connect_to_page('https://www4.sii.cl/consdcvinternetui/#/index', response_login)
# soup = BeautifulSoup(resp.text, 'html.parser')
# title = soup.find('h1')
# title
