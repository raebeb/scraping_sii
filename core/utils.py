import uuid
import requests

from core.sii_user import SiiUser
from core.rut import rut_to_dict

def create_UUID():
    return str(uuid.uuid4())

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