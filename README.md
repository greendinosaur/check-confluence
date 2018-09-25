# check-confluence
Simple python classes that check a given Confluence URL based on the pageid, space, page title, attachment name, shortURL exists

Example usage:
from ConfluenceRequest import ConfluenceRequest
from ConfluenceRequestHelper import ConfluenceRequestHelper

username = input("username?")
password = input("password?")
confluence_req = ConfluenceRequest(username, password)

test = ConfluenceRequestHelper(confluence_req, pageid='3670017')
print(str(test.does_confluence_reference_exist()))
