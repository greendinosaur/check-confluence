# check-confluence
Simple python classes that check a given Confluence URL exists on a server.

To use:
* ensure there is a *config.ini* file in the root folder with the parameters set correctly. This is used to define the Confluence instance to call. Check out the *EXAMPLEconfig.ini* file for the parameters
* Pass in the username and password used to authenticate against Confluence into an instance of *ConfluenceRequest*
* Pass in the URL (or other parameters such as page name, shorturl) to an instance of *ConfluenceRequestHelper*
# Example usage
```
from ConfluenceRequest import ConfluenceRequest
from ConfluenceRequestHelper import ConfluenceRequestHelper

username = input("username?")
password = input("password?")
confluence_req = ConfluenceRequest(username, password)

test = ConfluenceRequestHelper(confluence_req, pageid='3670017')
print(str(test.does_confluence_reference_exist()))
```