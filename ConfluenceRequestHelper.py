import json
from ConfluenceRequest import ConfluenceRequest
import configparser

class ConfluenceRequestHelper:

    config = configparser.ConfigParser()
    config.read('config.ini')

    api_url_base = config['DEFAULT']['BASE_URL']
    api_base_content = config['DEFAULT']['BASE_CONTENT']

    print(api_url_base)

    def __init__(self, confluence_request, pageid='', pagetitle='', space='', attachment='', tinyurl=''):
        """

        :type confluence_request: ConfluenceRequest
        """
        self.pageid = pageid
        self.pagetitle = pagetitle
        self.space = space
        self.attachment = attachment
        self.tinyurl = tinyurl
        self.con_req = confluence_request

        if self.pageid is not '' and self.attachment is not '':
            self.request_type = 1
        elif self.pageid is not '':
            self.request_type = 2
        elif self.pagetitle is not '' and self.space is not '':
            self.request_type = 3
        elif self.tinyurl is not '':
            self.request_type = 4

        self.request_url = self.format_url_to_check()


    def format_url_to_check(self):

        if self.request_type == 1:
            # this gets hold of all attachments on the page, still need to check the attachment is referenced
            return '{0}/{1}/child/attachment'.format(ConfluenceRequestHelper.api_url_base, self.pageid)

        if self.request_type == 2:
            return '{0}/{1}'.format(ConfluenceRequestHelper.api_url_base, self.pageid)

        if self.request_type == 3:
            return '{0}?spaceKey={1}&title={2}'.format(ConfluenceRequestHelper.api_url_base, self.space, self.pagetitle)

        if self.request_type == 4:
            # also need to consider tinyurl, bit more complex, may have to request the page, do the redirect to get the
            # pageid and then call the API again with the page id
            return '{0}/{1}'.format(ConfluenceRequestHelper.api_base_content, self.tinyurl)

        return None

    def does_attachment_exist(self, resp_json):
        # Need to loop through the JSON of attachments on a page and check one contains the named attachment
        for attachment in resp_json['results']:
            if attachment['title'] == self.attachment:
                return True

        return False


    def does_page_exist(self, resp_json):
        """

        :type resp_json: json
        """
        if resp_json is not None:
            if 'results' in resp_json:
                if 'type' in resp_json['results'][0]:
                    return True
            elif resp_json['type'] == 'page':
                return True

        return False


    def does_confluence_reference_exist(self):

        # check to see if the reference does exist
        if self.request_type == 4:
            return self.con_req.request_url(self.request_url)

        json_resp = self.con_req.request_api(self.request_url)
        if json_resp is not None:
            if self.request_type == 1:
                return self.does_attachment_exist(json_resp)
            else:
                return self.does_page_exist(json_resp)

        return False
