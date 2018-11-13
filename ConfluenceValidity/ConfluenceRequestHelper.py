import configparser
import json
import re
import os

from ConfluenceValidity.ConfluenceRequest import ConfluenceRequest


class ConfluenceRequestHelper:

    config = configparser.ConfigParser()
    new_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../config.ini')
    config.read(new_path)

    api_url_base = config['DEFAULT']['BASE_URL']
    api_base_content = config['DEFAULT']['BASE_CONTENT']

    def __init__(self, confluence_request, pageid='', pagetitle='', space='', attachment='', tinyurl='', url=''):
        """

        :type confluence_request: ConfluenceRequest
        :type pageid: String
        :type pagetitle: String
        :type space: String
        :type attachment: String
        :type tinyurl: String
        :type url: String
        """

        # if an actual URL is provided then use that to set the class properties
        # otherwise, use the other provided parameters
        self.initial_url = url
        self.pageid = pageid
        self.pagetitle = pagetitle
        self.space = space
        self.attachment = attachment
        self.tinyurl = tinyurl
        self.request_type = -1

        if self.initial_url is not '':
            self.set_data_from_url(self.initial_url)

        self.con_req = confluence_request
        self.request_url = None

        self.determine_request_type()

        self.format_url_to_check()

    def parse_url(self, url_to_test):
        """
        Parses the URL to determine its parameters and then sets the class variables accordingly
        :param url_to_test: the URL to parse
        :type url_to_test: String
        :return:
        """
        # pattern1 gives the pageID - so case 2
        # pattern2 gives the page reference and attachment name - case 1
        # pattern3 gives the space name and pagename - case 3
        # pattern4 gives the pageid - so case 2
        # pattern5 gives the short URL - case 4
        # pattern6 gives the space name and pagename - case 3

        #print(parse.urlsplit(url_to_test))
        #scheme gives whether it is http or https, netloc gives the url, path gives the rest
        #should then get hold of the first bit of text between the / and / on the path as this
        #gives the remainder as to whether it is wiki or page
        #can then use this rather than hardcoding the base URL as a config parameter
        #could also look to amend the regex to look for the string beginning with http and ending in /

        pattern1 = re.compile(r'(/pages/viewpage.action\?pageId=)(\d+)')
        pattern2 = re.compile(r'(/download/attachments/)(\d+)/([^?]*)')
        pattern3 = re.compile(r'(/display/)([a-zA-Z0-9%\+]*)/([^?]*)')
        pattern4 = re.compile(r'(/pages/viewpageattachments.action\?pageId=)(\d+)')
        pattern5 = re.compile(r'(/x)(.*)')
        pattern6 = re.compile(r'(/spaces/)([a-zA-Z0-9%\+]*)/pages/(\d+)/([^?]*)')

        match = re.search(pattern1, url_to_test)
        if match:
            self.pageid = match.groups()[1]
            return

        match = re.search(pattern2, url_to_test)
        if match:
            self.pageid = match.groups()[1]
            self.attachment = match.groups()[2]
            return

        match = re.search(pattern3, url_to_test)
        if match:
            self.space = match.groups()[1]
            self.pagetitle = match.groups()[2]
            return

        match = re.search(pattern6, url_to_test)
        if match:
            self.space = match.groups()[1]
            self.pagetitle = match.groups()[3]
            return

        match = re.search(pattern4, url_to_test)
        if match:
            self.pageid = match.groups()[1]
            return

        match = re.search(pattern5, url_to_test)
        if match:
            self.tinyurl = match.group()
            return

    def determine_request_type(self):
        """
        Determine the type of request type based on the parameters in the URL provided
        :return:
        """
        if self.pageid is not '' and self.attachment is not '':
            self.request_type = 1
        elif self.pageid is not '':
            self.request_type = 2
        elif self.pagetitle is not '' and self.space is not '':
            self.request_type = 3
        elif self.tinyurl is not '':
            self.request_type = 4

    def set_data_from_url(self, url):
        """
        Sets the class variables based on the data in the URL
        :param url: the URL to parse
        :type url: String
        :return:
        """
        self.parse_url(url)
        self.determine_request_type()

    def format_url_to_check(self):
        """
        Calculates the API call to make in order to validate the URL provided
        :return:
        """
        if self.request_type == 1:
            # this gets hold of all attachments on the page, still need to check the attachment is referenced
            self.request_url = '{0}/{1}/child/attachment'.format(ConfluenceRequestHelper.api_url_base, self.pageid)

        if self.request_type == 2:
            self.request_url = '{0}/{1}/version'.format(ConfluenceRequestHelper.api_url_base, self.pageid)

        if self.request_type == 3:
            self.request_url = '{0}?spaceKey={1}&title={2}'.format(ConfluenceRequestHelper.api_url_base, self.space,
                                                                   self.pagetitle)

        if self.request_type == 4:
            self.request_url = '{0}/{1}'.format(ConfluenceRequestHelper.api_base_content, self.tinyurl)

    def does_attachment_exist(self, resp_json):
        """
        Checks to see if the attachment is referenced in the JSON
        :param resp_json: the json to be examined
        :type resp_json: json
        :return:
        """
        # Need to loop through the JSON of attachments on a page and check one contains the named attachment
        if 'results' in resp_json:
            for attachment in resp_json['results']:
                if attachment['title'] == self.attachment:
                    return True

        return False

    def does_page_exist(self, resp_json):
        """
        Checks to see if the page is referenced in the JSON
        :param resp_json: the json to be examined
        :type resp_json: json
        """
        if resp_json is not None:
            if 'results' in resp_json:
                if len(resp_json['results']) > 0:
                    if 'type' in resp_json['results'][0]:
                        return True
                    elif 'by' in resp_json['results'][0]:
                        return True
            elif 'type' in resp_json:
                if resp_json['type'] == 'page':
                    return True
                elif resp_json['type'] == 'url':
                    return True

        return False

    def does_confluence_reference_exist(self):
        """
        Calls the Confluence API to see if the supplied page does exist
        :return: a boolean to indicate whether the provided URL does exist
        """
        if self.request_type > -1:
            json_resp = {}
            if self.request_type == 4:
                json_resp = self.con_req.request_url(self.request_url)
            else:
                json_resp = self.con_req.request_api(self.request_url)

            if json_resp is not None:
                if self.request_type == 1:
                    return self.does_attachment_exist(json_resp)
                elif self.request_type == 2 or self.request_type == 3 or self.request_type == 4:
                    return self.does_page_exist(json_resp)

        return False

