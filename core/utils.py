import uuid
import requests

from core.sii_user import SiiUser
from core.rut import rut_to_dict

def create_UUID():
    return str(uuid.uuid4())

def get_company_data(sii_user):
    response = sii_user.session.get('https://misiir.sii.cl/cgi_misii/siihome.cgi#')
    user_data = {
      "legal_representative": [
        {"name": '', "rut": '', "from_date": '' }, 
        ],
      "constitution_date": '',
      "start_of_activities": '',
      "full_address": '',
      "current_partners": [
        {
            "name": '',
            "rut": '',
            "aware_capital": 0, 
            "capital_to_find_out": 0,
            "capital_percentage": 0.0, 
            "percente_utilities": 0.0, 
            "membership_from": '' 
        }
        ],
      "active_economic_activities": 
        [
            {
                "code": '',
                "name": '',
                "category": 0, 
                "taxable": True,
                "start_at": ''
            }
        ],
      "characteristics": 
        [
            {
                "start_at": '', 
                "description": ''
            }
        ],
    }

def download_buying_book(sii_user: SiiUser, year: int, month: int, operation: str):
    url = 'https://www4.sii.cl/consdcvinternetui/services/data/facadeService/getResumen'
    payload = {
        "metaData": {
            "namespace": "cl.sii.sdi.lob.diii.consdcv.data.api.interfaces.FacadeService/getResumen",
            "conversationId": sii_user.token,
            "transactionId": create_UUID(),
            "page": None
        },
        'data': {
            "rutEmisor": rut_to_dict(sii_user.rut)['rut'],
            "dvEmisor": rut_to_dict(sii_user.rut)['dv'],
            "ptributario": f'{year}{month}',
            "estadoContab": "REGISTRO",
            "operacion": operation,
            "busquedaInicial": True
    
        }
    }
    print(f'PAYLOAD ---> {payload}')
    
    response = sii_user.session.post(url, data=payload)
    return response
