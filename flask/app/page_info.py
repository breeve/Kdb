
class searchNormalItem:
    srcDB = 'Default'
    title = 'Default'
    author = 'Default'
    organ = 'Default'
    source = 'Default'
    keyword = ['default1', 'default']
    summary = "Default String.....etc"


class pageInfo:
    current_page = 0
    total_page = 0
    total_rows = []
    rows = []

def getPageInfo():
    page_info = pageInfo()
    return page_info