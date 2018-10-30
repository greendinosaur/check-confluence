from behave import *
import ast
import os
from ConfluenceValidity.ConfluenceRequestHelper import ConfluenceRequestHelper
from ConfluenceValidity.ConfluenceRequest import ConfluenceRequest


@given('a Confluence {URL}')
def step_impl(context, URL):
    context.url = URL
    pass


@when('a user requests it')
def step_impl(context):
    conf_req = ConfluenceRequest(os.environ.get('CONF_UNAME'), os.environ.get('CONF_PWORD'))
    conf_helper = ConfluenceRequestHelper(conf_req, url=context.url)
    # store the next value in the context as this will call the API and return a Boolean as to whether it exists or not
    context.does_ref_exist = conf_helper.does_confluence_reference_exist()
    pass


@then('it {exists}')
def step_impl(context, exists):
    # now evaluate the value in the context to see if matches the supplied parameter
    assert (context.does_ref_exist == ast.literal_eval(exists))
