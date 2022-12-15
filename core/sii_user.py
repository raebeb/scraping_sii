from bs4 import BeautifulSoup
import requests

from .rut import rut_to_dict

class SiiUser:
    def __init__(self, rut, password):
        self.rut = rut
        self.password = password
        self.session = self.login(self.rut, self.password)
        self.cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
        self.token = self.cookies['TOKEN']


    def create_data_for_login(self, rut, password):
        data = rut_to_dict(rut)

        return {
            'rut': data["rut"],
            'dv': data["dv"],
            'referencia': 'https://misiir.sii.cl/cgi_misii/siihome.cgi',
            '411': '',
            'rutcntr': data["rutcntr"],
            'clave': password,
        }

    def login(self, rut, password):
        session_requests = requests.Session()

        data = self.create_data_for_login(rut, password)
        response = session_requests.post('https://zeusr.sii.cl/cgi_AUT2000/CAutInicio.cgi', data=data)

        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.find(id="auth_bottom"):
            print("Login unsuccessful")
            return False
        print("Login successful")

        return session_requests

    def logout(self):
        requests.cookies.clear(domain=None, path=None, name=None)


    def connect_to_page(self, url: str, session: requests.Session):
        if session:
            return session.get(url)
        return False


# python manage.py shell
# from core.utils import *
# response_login = login_to_sii('782413708', 'union2')

# {
#     "metaData": {
#         "namespace": "cl.sii.sdi.lob.diii.consdcv.data.api.interfaces.FacadeService/getResumen",
#         "conversationId": "TVXI8WXPLZO37",
#         "transactionId": "a7fb7d5d-ebb3-451d-a43d-623feafe4140",
#         "page": null
#     },
#     "data": {
#         "rutEmisor": "78241370",
#         "dvEmisor": "8",
#         "ptributario": "202212",
#         "estadoContab": "REGISTRO",
#         "operacion": "COMPRA",
#         "busquedaInicial": true
#     }
# }

# function createUUID() {
#     for (var a = [], b = "0123456789abcdef", c = 0; 36 > c; c++)
#         a[c] = b.substr(Math.floor(16 * Math.random()), 1);
#     a[14] = "4",
#     a[19] = b.substr(3 & a[19] | 8, 1),
#     a[8] = a[13] = a[18] = a[23] = "-";
#     var d = a.join("");
#     return d
# }