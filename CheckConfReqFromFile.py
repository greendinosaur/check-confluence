import openpyxl
import os

from ConfluenceValidity.ConfluenceRequest import ConfluenceRequest
from ConfluenceValidity.ConfluenceRequestHelper import ConfluenceRequestHelper

FILE_READ = 'urlstotest1.xlsx'  # The Excel file to read
COL_TO_READ = 1  # The column containing the URL, starts at 0
COL_TO_WRITE = 2  # The column to write out the result
UNAME = os.environ.get('CONF_UNAME') #usernamr for confluence access
PWORD = os.environ.get('CONF_PWORD') #password for confluence access


def check_conf_URL(conf_req, url):
    # Checks whether the given URL exists
    conf_req_help = ConfluenceRequestHelper(confluence_request=conf_req, url=url)
    is_valid = conf_req_help.does_confluence_reference_exist()
    return is_valid


def check_URLs_from_file(filename):
    # Looks through the Excel file, checks each URL in turn and outputs whether it exists
    conf_req = ConfluenceRequest(UNAME, PWORD)
    wb = openpyxl.load_workbook(filename)
    sheet = wb.active

    for row in sheet.rows:
        url = row[COL_TO_READ].value
        if url is not None:
            row[COL_TO_WRITE].value = check_conf_URL(conf_req, url)

    wb.save('out_' + filename)
    wb.close()
    return


# main part of the script to execute
def main():
    check_URLs_from_file(FILE_READ)


if __name__ == "__main__":
    main()