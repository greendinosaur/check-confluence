# 3rd party modules
from flask import make_response, abort

import os

from ConfluenceValidity.ConfluenceRequestHelper import ConfluenceRequestHelper
from ConfluenceValidity.ConfluenceRequest import ConfluenceRequest

def check_validity(url):
    conf_req = ConfluenceRequest(os.environ.get('CONF_UNAME'), os.environ.get('CONF_PWORD'))
    conf_helper = ConfluenceRequestHelper(conf_req, url=url)
    # store the next value in the context as this will call the API and return a Boolean as to whether it exists or not
    does_ref_exist = conf_helper.does_confluence_reference_exist()
    return {"exists": does_ref_exist}