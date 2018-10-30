Feature: Check URL Exists
  # This tests some real URLs for being valid Confluence references

  #https://devaardvark.atlassian.net/wiki/spaces/DEV/pages/3670017/test+page+with+attachment
  #https://devaardvark.atlassian.net/wiki/download/attachments/3670017/apple-logo_318-40184.jpg?api=v2
#https://devaardvark.atlassian.net/wiki/x/AQA4
  #https://devaardvark.atlassian.net/wiki/pages/viewpage.action?pageId=3866626

  Scenario Outline: Test URLs
    # Enter steps here
    Given a Confluence <URL>
    When a user requests it
    Then it <exists>

    Examples: Valid URLs - pageid only
    | URL                                         | exists |
    | /wiki/pages/viewpage.action?pageId=3866626  | True  |

    Examples: Valid URLs - space and page
    | URL                                                         | exists |
    | /wiki/spaces/DEV/pages/3670017/test+page+with+attachment    | True |

    Examples: Valid URLs - attachment
    | URL                                                                   | exists |
    | /wiki/download/attachments/3670017/apple-logo_318-40184.jpg?api=v2    | True |

    Examples: Valid URLs - tinyURL
    | URL                                             | exists |
    | /wiki/x/AQA4                                    | True |

    Examples: Invalid URLs
    | URL                                               | exists |
    | /wiki/x/AQA412345                                 | False |
    |  /wiki/pages/viewpage.action?pageId=31266626      | False |
    | http://www.google.com                             | False |
