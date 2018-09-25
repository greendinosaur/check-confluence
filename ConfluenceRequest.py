import json
import requests


class ConfluenceRequest:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def request_url(self, url_to_get):
        response = requests.get(url_to_get, auth=(self.username, self.password))

        if response.status_code == 200:
            return True
        else:
            return False

    def request_api(self, api_url):
        response = requests.get(api_url, auth=(self.username, self.password))

        if response.status_code == 200:
            if response.headers['Content-Type'] == 'application/json':
                return json.loads(response.content.decode('utf-8'))

        return None
