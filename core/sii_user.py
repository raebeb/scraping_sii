from bs4 import BeautifulSoup
import requests

from .rut import rut_to_dict


class SiiUser:
    def __init__(self, rut, password):
        self.rut = rut
        self.password = password
        self.session = self.login(self.rut, self.password)
        self.cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
        self.token = self.cookies["TOKEN"]

    def create_data_for_login(self, rut, password):
        data = rut_to_dict(rut)

        return {
            "rut": data["rut"],
            "dv": data["dv"],
            "referencia": "https://misiir.sii.cl/cgi_misii/siihome.cgi",
            "411": "",
            "rutcntr": data["rutcntr"],
            "clave": password,
        }

    def login(self, rut, password):
        session_requests = requests.Session()

        data = self.create_data_for_login(rut, password)
        response = session_requests.post(
            "https://zeusr.sii.cl/cgi_AUT2000/CAutInicio.cgi", data=data
        )

        soup = BeautifulSoup(response.text, "html.parser")
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
