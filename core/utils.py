import re
import ast
import json
import uuid
import requests
import urllib.request

from bs4 import BeautifulSoup

from core.sii_user import SiiUser
from core.rut import rut_to_dict


def create_UUID():
    return str(uuid.uuid4())


def get_company_data(sii_user: SiiUser) -> dict:
    """
    This method is used to get the company data from the SII and create the body to send to the API

    Args:
        sii_user (SiiUser): SiiUser object

    Returns:
        dict: Body requested by frontend
    """

    response = sii_user.session.get("https://misiir.sii.cl/cgi_misii/siihome.cgi#")
    soup = BeautifulSoup(response.content, "html.parser")

    ### Here we extract the data from the script tag
    scripts = soup.find_all("script")
    for script in scripts:
        if "DatosCntrNow" in script.text:
            contributor_data = script

    ### Here we delete all the white spaces and the variables names
    clean_data = (
        contributor_data.text.replace("\t", "")
        .replace("\r", "")
        .replace("\n", "")
        .replace("DatosCntrNow", "")
        .replace(";", "")
        .replace("DatosCntrAler", "")
        .replace("DatosActeco", "")
    )

    ### Here we split the data in a list of strings
    data_without_name_variables = clean_data.split("=")

    ### Here we set the data to the variables
    # Im using the same variable name that is used in the SII but im don't have idea what tf they mean
    datos_cntr_now = json.loads(data_without_name_variables[1])
    datos_cntr_aler = json.loads(data_without_name_variables[2])
    datos_acteco = json.loads(data_without_name_variables[3])

    # Get data for legal representative
    data = {
        "opc": "112",
    }

    response = sii_user.session.post(
        "https://misiir.sii.cl/cgi_misii/CViewCarta.cgi",
        cookies=sii_user.cookies,
        data=data,
    )

    json_response = json.loads(response.content.decode("utf-8"))

    legal_representatives = json_response["representantes"]
    current_partners = json_response["socios"]

    # Get data for active economic activities
    data = {
        "year": "",
        "opc": "21",
        "VIEW": "1",
    }
    response = sii_user.session.post(
        "https://misiir.sii.cl/cgi_misii/CViewCarta.cgi",
        cookies=sii_user.cookies,
        data=data,
    )

    json_response = json.loads(response.content.decode("utf-8"))
    activities = json_response["listHistoricoGiros"]
    # print(f"RESPONSE ? -----> {json.dumps(json_response)}")

    # Get data for caracteristics
    characteristics = datos_cntr_now["atributos"]

    soup = BeautifulSoup(response.content, "html.parser")

    user_data = {
        "legal_representative": [
            {
                "name": f"{representative['nombres']} {representative['apellidoPaterno']} {representative['apellidoMaterno']}",
                "rut": f"{representative['rut']}-{representative['dv']}",
                "from_date": representative["fechaInicio"],
            }
            for representative in legal_representatives
        ],
        "constitution_date": datos_cntr_now["contribuyente"]["fechaConstitucion"],
        "start_of_activities": datos_cntr_now["contribuyente"][
            "fechaInicioActividades"
        ],
        "full_address": datos_cntr_now["contribuyente"]["unidadOperativaDireccion"],
        "current_partners": [
            {
                "name": f"{partner['nombres']} {partner['apellidoPaterno']} {partner['apellidoMaterno']}",
                "rut": f"{partner['rut']}-{partner['dv']}",
                "aware_capital": int(partner["aporteEnterado"]),
                "capital_to_find_out": int(partner["aportePorEnterar"]),
                "capital_percentage": float(partner["participacionCapital"]),
                "percentage_utilities": float(partner["participacionUtilidades"]),
                "membership_from": partner["fechaIncorporacion"],
            }
            for partner in current_partners
        ],
        "active_economic_activities": [
            {
                "code": activity["tacnCodigo"],
                "name": activity["tacnDesc"],
                "category": int(activity["categoriaTributaria"]),
                "taxable": False if activity["afectaIva"] == "N" else True,
                "start_at": activity["fechaInicio"],
            }
            for activity in activities
        ],
        "characteristics": [
            {
                "start_at": characteristic["fechaInicio"],
                "description": characteristic["descAtrCodigo"],
            }
            for characteristic in characteristics
        ],
    }
    return user_data


def download_buying_book(sii_user: SiiUser, year: int, month: int, operation: str):
    url = "https://www4.sii.cl/consdcvinternetui/services/data/facadeService/getResumen"
    payload = {
        "metaData": {
            "namespace": "cl.sii.sdi.lob.diii.consdcv.data.api.interfaces.FacadeService/getResumen",
            "conversationId": sii_user.token,
            "transactionId": create_UUID(),
            "page": None,
        },
        "data": {
            "rutEmisor": rut_to_dict(sii_user.rut)["rut"],
            "dvEmisor": rut_to_dict(sii_user.rut)["dv"],
            "ptributario": f"{year}{month}",
            "estadoContab": "REGISTRO",
            "operacion": operation,
            "busquedaInicial": True,
        },
    }
    print(f"PAYLOAD ---> {payload}")

    response = sii_user.session.post(url, data=payload)
    return response
