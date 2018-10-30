import json
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from ConfluenceValidity.ConfluenceRequest import ConfluenceRequest


class TestConfluenceRequest(unittest.TestCase):

    @patch('requests.get', autospec=True)
    def test_request_url_valid_status_code(self, request_mock):
        """
        checks that if a valid status code is returned for a URL then this is detected correctly
        :param request_mock:
        :return:
        """
        request_mock.return_value = MagicMock(status_code=200)
        conf_req = ConfluenceRequest(username="user", password="pass")
        url_data = conf_req.request_url("test")
        self.assertTrue(url_data == {"type": "page"})

    @patch('requests.get', autospec=True)
    def test_request_url_invalid_status_code(self, request_mock):
        """
        checks that if an invalid status code is provided when requesting a URL then empty JSON is returned
        :return:
        """
        request_mock.return_value = MagicMock(status_code=100)
        conf_req = ConfluenceRequest(username="user", password="pass")
        url_data = conf_req.request_url("test")
        self.assertTrue(url_data == {})

    @patch('requests.get', autospec=True)
    def test_request_api_valid_status_code(self, request_mock):
        """
        checks that if a valid response is given then JSON is returned
        :param request_mock:
        :return:
        """
        m1 = MagicMock(decode=MagicMock(return_value=json.dumps({"type": "page"})))
        request_mock.return_value = MagicMock(status_code=200,
                                              headers={'Content-Type': 'application/json'},
                                              content=m1)
        conf_req = ConfluenceRequest(username="user", password="pass")
        api_data = conf_req.request_api("testapi")
        self.assertTrue(api_data == {"type": "page"})

    @patch('requests.get', autospec=True)
    def test_request_api_invalid_status_code(self, request_mock):
        """
        checks that is an invalid status code is provided when requesting an API then empty JSON is returned
        :return:
        """
        request_mock.return_value = MagicMock(status_code=100)
        conf_req = ConfluenceRequest(username="user", password="pass")
        url_data = conf_req.request_api("test")
        self.assertTrue(url_data == {})

    @patch('requests.get', autospec=True)
    def test_request_api_invalid_header(self, request_mock):
        """
        checks that if an invalid header is returned then empty JSON is returned
        :param request_mock:
        :return:
        """
        m1 = MagicMock(decode=MagicMock(return_value=json.dumps({"type": "page"})))
        request_mock.return_value = MagicMock(status_code=200,
                                              headers={'Content-Type': 'dhhddh'},
                                              content=m1)
        conf_req = ConfluenceRequest(username="user", password="pass")
        api_data = conf_req.request_api("testapi")
        self.assertTrue(api_data == {})


if __name__ == '__main__':
    unittest.main()
