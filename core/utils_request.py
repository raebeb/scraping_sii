import re
import ast
import json
import uuid
import requests
import urllib.request

from core.sii_user import SiiUser


def format_response(response: requests.Response) -> dict:
    """
    This method is used to format the response from the SII

    Args:
        response (requests.Response): Response from the SII

    Returns:
        dict: Response formatted
    """
    return json.loads(response.content.decode("utf-8"))


def request_post(sii_user: SiiUser, url: str, cookies, data: dict) -> dict:
    """
    This method is used to send a post request to the SII

    Args:
        url (str): URL to send the request
        cookies (dict): Cookies to send with the request
        data (dict): Data to send with the request

    Returns:
        requests.Response: Response from the SII
    """
    return format_response(
        sii_user.session.post(
            url,
            cookies=cookies,
            data=data,
        )
    )
