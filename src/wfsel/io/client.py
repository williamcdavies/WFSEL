"""
Filename:   wfsel.io.clients.py
Author:     William Chuter-Davies
"""

# Related Third-party Imports
import requests


def get(
    url: str,
) -> requests.Response:
    """
    Submit an HTTP GET request.

    Parameters
    ----------
    url : str
        The URL

    Returns
    -------
    requests.Response
        The response
    """
    response = requests.get(url, timeout = 30)

    response.raise_for_status()

    return response
