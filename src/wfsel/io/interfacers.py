"""
Filename:   wfsel.io.interfacers.py
Author:     William Chuter-Davies
Modified:   10/11/26
"""

# Related Third-party Imports
import requests


def download(
    url: str,
) -> bytes:
    """
    Submit an HTTP GET request and return the response as bytes.

    Parameters
    ----------
    url : str
        The URL

    Returns
    -------
    bytes
        The bytes
    """
    r = requests.get(url, timeout = 30)

    r.raise_for_status()

    c = r.content

    return c
