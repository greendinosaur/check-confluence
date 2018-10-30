import json
import requests


class ConfluenceRequest:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def request_url(self, url_to_get):
        """
        Calls the page directly as a normal HTTP Call
        :param url_to_get:
        :return:
        """
        response = requests.get(url_to_get, auth=(self.username, self.password))

        if response.status_code == 200:
            return {"type": "page"}

        return {}

    def request_api(self, api_url):
        """
        Calls the COnfluence API to retrieve data about the page
        :param api_url:
        :return:
        """
        response = requests.get(api_url, auth=(self.username, self.password))


        if response.status_code == 200:
            if response.headers['Content-Type'] == 'application/json':
                return json.loads(response.content.decode('utf-8'))

        return {}
