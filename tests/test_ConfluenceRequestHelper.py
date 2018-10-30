import unittest
from unittest import mock
from ConfluenceValidity.ConfluenceRequestHelper import ConfluenceRequestHelper


class TestConfluenceHelper(unittest.TestCase):

    def test_determine_request_type_attachment(self):
        """
        tests that the type of data is correctly determined based on the objects attributes for an attachment
        :return:
        """
        conf_reg_helper = ConfluenceRequestHelper(confluence_request=None, pageid='123', attachment='ABCD')
        self.assertTrue(conf_reg_helper.request_type == 1)

    def test_format_url_attachment(self):
        """
        tests that the URL used to call the API is correct when an attachment is referenced
        :return:
        """
        conf_reg_helper = ConfluenceRequestHelper(confluence_request=0, pageid='123', attachment='ABCD')
        self.assertTrue('123' in conf_reg_helper.request_url)
        self.assertTrue('123/child/attachment' in conf_reg_helper.request_url)

    def test_does_attachment_exist(self):
        """
        tests that JSON is correctly parsed for the given attachment
        :return:
        """
        conf_reg_helper = ConfluenceRequestHelper(confluence_request=0, pageid='123', attachment='ABCD')
        test_json = {"results": [{"title": "ABCD"}]}
        self.assertTrue(conf_reg_helper.does_attachment_exist(test_json))

    def test_does_attachment_exist_invalid(self):
        """
        tests that invalid JSON for an attachment is recognised as invalid
        :return:
        """
        conf_reg_helper = ConfluenceRequestHelper(confluence_request=0, pageid='123', attachment='ABCD')
        test_json = {"results": [{"title": "ABCDEFG"}]}
        self.assertFalse(conf_reg_helper.does_attachment_exist(test_json))

    def test_determine_request_type_tinyurl(self):
        """
        tests that the tinyURL case is correctly determined from the object attributes
        :return:
        """
        conf_reg_helper = ConfluenceRequestHelper(confluence_request=0, tinyurl='123')
        self.assertTrue(conf_reg_helper.request_type == 4)

    def test_format_url_tinyurl(self):
        """
        tests that the URL for the API call is correct for a tinyurl
        :return:
        """
        conf_reg_helper = ConfluenceRequestHelper(confluence_request=0, tinyurl='123')
        self.assertTrue('123' in conf_reg_helper.request_url)
        self.assertTrue('/123' in conf_reg_helper.request_url)

    def test_determine_request_type_space(self):
        """
        tests that the type of request is determined for the space case
        :return:
        """
        conf_reg_helper = ConfluenceRequestHelper(confluence_request=0, pagetitle='123', space='ABC')
        self.assertTrue(conf_reg_helper.request_type == 3)

    def test_format_url_space(self):
        """
        tests the API is correct for when a space and pagetitle is required
        :return:
        """
        conf_reg_helper = ConfluenceRequestHelper(confluence_request=0, pagetitle='123', space='ABC')
        self.assertTrue('123' in conf_reg_helper.request_url)
        self.assertTrue('ABC' in conf_reg_helper.request_url)
        self.assertTrue('?spaceKey=ABC&title=123' in conf_reg_helper.request_url)

    def test_determine_request_type_pageid(self):
        """
        tests the type of query is determined for when a pageid is present
        :return:
        """
        conf_reg_helper = ConfluenceRequestHelper(confluence_request=0, pageid='123')
        self.assertTrue(conf_reg_helper.request_type == 2)

    def test_format_url_pageid(self):
        """
        tests the url for the API call is correct for when a pageid is present
        :return:
        """
        conf_reg_helper = ConfluenceRequestHelper(confluence_request=0, pageid='123')
        self.assertTrue('123' in conf_reg_helper.request_url)
        self.assertTrue('/123' in conf_reg_helper.request_url)

    def test_does_page_exist_results(self):
        """
        checks that valid JSON for an existing page is determined correctly
        :return:
        """
        conf_reg_helper = ConfluenceRequestHelper(confluence_request=0, pageid='123', attachment='ABCD')
        test_json = {"type": "page"}
        self.assertTrue(conf_reg_helper.does_page_exist(test_json))
        test_json = {"type": "url"}
        self.assertTrue(conf_reg_helper.does_page_exist(test_json))

    def test_does_page_exist_results_invalid(self):
        """
        checks that invalid JSON for a page is determined as being invalid
        :return:
        """
        conf_reg_helper = ConfluenceRequestHelper(confluence_request=0, pageid='123', attachment='ABCD')
        test_json = {"type1213": "page"}
        self.assertFalse(conf_reg_helper.does_page_exist(test_json))

    def test_does_page_exist_type(self):
        """
        checks that the JSON used to indicate an attachment on a page exists is correctly parsed
        :return:
        """
        conf_reg_helper = ConfluenceRequestHelper(confluence_request=0, pageid='123', attachment='ABCD')
        test_json = {"results": [{"type": "ABCDEFG"}]}
        self.assertTrue(conf_reg_helper.does_page_exist(test_json))

    def test_does_page_exist_type_invalid(self):
        """
        checks that invalid JSON for an attachment on a page is determined as invalid
        :return:
        """
        conf_reg_helper = ConfluenceRequestHelper(confluence_request=0, pageid='123', attachment='ABCD')
        test_json = {"results": [{"typeasd": "ABCDEFG"}]}
        self.assertFalse(conf_reg_helper.does_page_exist(test_json))

        test_json = {"resultsdddd": [{"typeasd": "ABCDEFG"}]}
        self.assertFalse(conf_reg_helper.does_page_exist(test_json))

        test_json = {}
        self.assertFalse(conf_reg_helper.does_page_exist(test_json))

    def test_parse_URL_valid(self):
        """
        tests that the URL is parsed into its constituent parts correctly
        :return:
        """
        conf_reg_helper = ConfluenceRequestHelper(confluence_request=0)
        conf_reg_helper.parse_url(url_to_test='https://somesite.com/pages/viewpage.action?pageId=98765')
        self.assertTrue(conf_reg_helper.pageid == '98765')

        conf_reg_helper.parse_url(url_to_test='https://somesite.com/pages/download/attachments/456/someattachment?')
        self.assertTrue(conf_reg_helper.pageid == '456')
        self.assertTrue(conf_reg_helper.attachment == 'someattachment')

        conf_reg_helper.parse_url(url_to_test='https://somesite.com/pages/display/somespace/somepage?')
        self.assertTrue(conf_reg_helper.space == 'somespace')
        self.assertTrue(conf_reg_helper.pagetitle == 'somepage')

        conf_reg_helper.parse_url(url_to_test='https://somesite.com/pages/wiki/spaces/DEV/pages/3670017/test+page+with+attachment?')
        self.assertTrue(conf_reg_helper.space == 'DEV')
        self.assertTrue(conf_reg_helper.pagetitle == 'test+page+with+attachment')

        conf_reg_helper.parse_url(url_to_test='https://somesite.com/pages/viewpageattachments.action?pageId=87654')
        self.assertTrue(conf_reg_helper.pageid == '87654')

        conf_reg_helper.parse_url(url_to_test='https://somesite.com/pages/xasder')
        self.assertTrue(conf_reg_helper.tinyurl == '/xasder')

    def test_set_data_from_url(self):
        """
        tests that the URL is parsed and the type of request is correctly determined
        :return:
        """
        conf_req_helper = ConfluenceRequestHelper(confluence_request=0)
        conf_req_helper.set_data_from_url('https://somesite.com/pages/viewpage.action?pageId=98765')
        self.assertTrue(conf_req_helper.request_type == 2)

        conf_req_helper = ConfluenceRequestHelper(confluence_request=0)
        conf_req_helper.set_data_from_url('https://somesite.com/pages/download/attachments/456/someattachment?')
        self.assertTrue(conf_req_helper.request_type == 1)

        conf_req_helper = ConfluenceRequestHelper(confluence_request=0)
        conf_req_helper.set_data_from_url('https://somesite.com/pages/display/somespace/somepage?')
        self.assertTrue(conf_req_helper.request_type == 3)

        conf_req_helper.set_data_from_url('https://somesite.com/wiki/spaces/DEV/pages/3670017/test+page+with+attachment?')
        self.assertTrue(conf_req_helper.request_type == 3)

        conf_req_helper = ConfluenceRequestHelper(confluence_request=0)
        conf_req_helper.set_data_from_url('https://somesite.com/pages/viewpageattachments.action?pageId=87654')
        self.assertTrue(conf_req_helper.request_type == 2)

        conf_req_helper = ConfluenceRequestHelper(confluence_request=0)
        conf_req_helper.set_data_from_url('https://somesite.com/xasder')
        self.assertTrue(conf_req_helper.request_type == 4)

    def test_invalid_constructor(self):
        """
        checks that the JSON used to indicate an attachment on a page exists is correctly parsed
        :return:
        """
        conf_reg_helper = ConfluenceRequestHelper(confluence_request=0)
        self.assertFalse(conf_reg_helper.does_confluence_reference_exist())


    def test_does_confluence_reference_exist_tinyurl(self):
        """
        Simulates a positive response from the API when given a tinyurl
        :return:
        """
        m = mock.Mock()
        m.request_url.return_value = {"type": "page"}
        conf_req_helper = ConfluenceRequestHelper(m, tinyurl='123')
        self.assertTrue(conf_req_helper.does_confluence_reference_exist())
        m.request_url.assert_called_with(conf_req_helper.request_url)

    def test_does_confluence_reference_exist_tinyurl_false(self):
        """
        Simulates a missing value response from the API when given a tinyurl
        :return:
        """
        m = mock.Mock()
        m.request_url.return_value = {}
        conf_req_helper = ConfluenceRequestHelper(m, tinyurl='123')
        self.assertFalse(conf_req_helper.does_confluence_reference_exist())

    def test_does_confluence_reference_exist_attachment(self):
        """
        simulates a positive response from the API when requesting an attachment
        :return:
        """
        m = mock.Mock()
        m.request_api.return_value = {"results": [{"title": "ABCD"}]}
        conf_req_helper = ConfluenceRequestHelper(m, pageid='123', attachment='ABCD')
        self.assertTrue(conf_req_helper.does_confluence_reference_exist())
        m.request_api.assert_called_with(conf_req_helper.request_url)

    def test_does_confluence_reference_exist_attachment_false(self):
        """
        simulates a negative response from the API when requesting an attachment
        :return:
        """
        m = mock.Mock()
        m.request_api.return_value = {}
        conf_req_helper = ConfluenceRequestHelper(m, pageid='123', attachment='ABCD')
        self.assertFalse(conf_req_helper.does_confluence_reference_exist())

    def test_does_confluence_reference_exist_page(self):
        """
        simulates a positive response from the API when reqeusting a page
        :return:
        """
        m = mock.Mock()
        m.request_api.return_value = {"type": "page"}
        conf_req_helper = ConfluenceRequestHelper(m, pageid='123')
        self.assertTrue(conf_req_helper.does_confluence_reference_exist())
        m.request_api.assert_called_with(conf_req_helper.request_url)

    def test_does_confluence_reference_exist_page_false(self):
        """
        simualtes a negative response from the API when requesting a page
        :return:
        """
        m = mock.Mock()
        m.request_api.return_value = {}
        conf_req_helper = ConfluenceRequestHelper(m, pageid='123')
        self.assertFalse(conf_req_helper.does_confluence_reference_exist())

    def test_does_confluence_reference_exist_space(self):
        """
        simulates a positive response from the API when requesting a page and space
        :return:
        """
        m = mock.Mock()
        m.request_api.return_value = {"type": "page"}
        conf_req_helper = ConfluenceRequestHelper(m, pagetitle='123', space='ABC')
        self.assertTrue(conf_req_helper.does_confluence_reference_exist())
        m.request_api.assert_called_with(conf_req_helper.request_url)

    def test_does_confluence_reference_exist_space_false(self):
        """
        simulates a negative response from the API when requesting a page and space
        :return:
        """
        m = mock.Mock()
        m.request_api.return_value = {}
        conf_req_helper = ConfluenceRequestHelper(m, pagetitle='123', space='ABC')
        self.assertFalse(conf_req_helper.does_confluence_reference_exist())


if __name__ == '__main__':
    unittest.main()
