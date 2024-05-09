import logging

import requests

logging.basicConfig(level=logging.INFO)


class Client:
    def send_request(self, method, url, headers=None, params=None):
        response = requests.request(method, url, headers=headers, params=params)
        return response
