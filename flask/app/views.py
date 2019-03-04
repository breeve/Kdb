import pymongo
import re
import math
import uuid
import time
from flask import render_template, flash, redirect, request
from app import app
from .forms import LoginForm
from .page_info import pageInfo, searchNormalItem

from .page_info import getPageInfo

ROWS_PER_PAGE = 10

g_name = ""
g_age  = 0
g_user_id = 0

def save_personal_time_start(user_id):
    start_time = time.localtime(time.time())
    print(str(user_id)+" start_time: "+str(start_time))

    client = pymongo.MongoClient(host='localhost', port=27017)
    K_db = client.K_db
    collection = K_db.personalTime

    keywords_regex = {}
    keywords_regex['user_id'] = user_id
    row = collection.find_one(keywords_regex)

    datax = {}
    datax['user_id'] = user_id
    datax['start_time'] = start_time

    if row :
        datax['end_time'] = row['end_time']
        collection.update(row, datax)
    else :
        datax['end_time'] = ''
        collection.insert_one(datax).inserted_id

    print(datax)


def save_personal_time_end(user_id):
    end_time = time.localtime(time.time())
    print(str(user_id)+" end_time: "+str(end_time))

    client = pymongo.MongoClient(host='localhost', port=27017)
    K_db = client.K_db
    collection = K_db.personalTime

    keywords_regex = {}
    keywords_regex['user_id'] = user_id
    row = collection.find_one(keywords_regex)

    datax = {}
    datax['user_id'] = user_id
    datax['end_time'] = end_time
    if row :
        datax['start_time'] = row['start_time']
        collection.update(row, datax)
    else :
        datax['start_time'] = ''
        collection.insert_one(datax).inserted_id

    print(datax)

def get_search_regex(key, keywords):
    keywords_regex = {}
    kws = [ks for ks in keywords.strip().split(' ') if ks != '']

    if len(kws) > 0:
        reg_pattern = re.compile('|'.join(kws), re.IGNORECASE)
        keywords_regex[key] = reg_pattern

    return keywords_regex

def get_search_result(keywords, page):
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['K_db']
    keywords_regex_summary = get_search_regex('Summary-摘要', keywords)
    #keywords_regex_title = get_search_regex('Title-题名', keywords)
    #keywords_regex_key_word = get_search_regex('Keyword-关键词', keywords)


    collection = db['maps_items']

    total_rows_summary = collection.find(keywords_regex_summary).count()
    #total_rows_title = collection.find(keywords_regex_title).count()
    #total_rows_key_word = collection.find(keywords_regex_key_word).count()
    '''
    print(total_rows_summary)
    print(total_rows_title)
    print(total_rows_key_word)
    '''

    total_page = int(math.ceil(total_rows_summary / (ROWS_PER_PAGE * 1.0)))
    #total_page += int(math.ceil(total_rows_title / (ROWS_PER_PAGE * 1.0)))
    #total_page += int(math.ceil(total_rows_key_word / (ROWS_PER_PAGE * 1.0)))

    page_info = {'current': page, 'total_page': total_page,
                 'total_rows': total_rows_summary, 'rows': []}

    if total_page > 0 and page <= total_page:
        row_start = (page - 1) * ROWS_PER_PAGE

        cursors = collection.find(keywords_regex_summary) \
            .skip(row_start).limit(ROWS_PER_PAGE)
        for c in cursors:
            if c not in page_info['rows']:
                page_info['rows'].append(c)

        '''
        cursors = collection.find(keywords_regex_title) \
            .skip(row_start).limit(ROWS_PER_PAGE)
        for c in cursors:
            page_info['rows'].append(c)

        cursors = collection.find(keywords_regex_key_word) \
            .skip(row_start).limit(ROWS_PER_PAGE)
        for c in cursors:
            page_info['rows'].append(c)
        '''

    '''
    print(keywords_regex_summary)
    print(keywords_regex_title)
    print(keywords_regex_key_word)
    print(page_info)
    '''

    rows = []

    tmp = set()
    for d in page_info['rows']:
        t = tuple(d.items())

        if t not in tmp:
            tmp.add(t)
            rows.append(d)

    page_info['rows'] = rows

    total_rows_summary = len(page_info['rows'])
    page_info['total_rows'] = total_rows_summary
    page_info['total_page'] = int(math.ceil(total_rows_summary / (ROWS_PER_PAGE * 1.0)))


    client.close()

    return page_info

def save_personalSearchInfo(name, age, keywords):
    client = pymongo.MongoClient(host='localhost', port=27017)
    K_db = client.K_db
    collection = K_db.personalSearchInfo
    datax = {}
    datax['name'] = name
    datax['age'] = age
    datax['keywords'] = keywords
    collection.insert_one(datax).inserted_id

def get_search_result_kinds(rows):
    keyword = []
    for r in rows:
        keyword.append(r['Keyword-关键词'])
    '''
    for key in keyword:
        print(key)
    '''

def get_left_row(page_info):
    keys = []
    for item in page_info.total_rows:
        for key in item["Classifier-类别"].split(';;'):
            keys.append(key.split('\n')[0])
    # print(list(set(keys)))

    return keys

@app.route("/search_profession_result")
def search_profession_result():
    keywords = request.args.get('keywords')
    name = g_name
    age = g_age
    page = int(request.args.get('page', 1))

    # get the total count and page:
    total_rows = get_search_result(keywords)
    total_page = int(math.ceil(total_rows.count() / (ROWS_PER_PAGE * 1.0)))

    page_info = getPageInfo()
    page_info.total_rows = total_rows
    page_info.total_page = total_page
    page_info.current_page = page

    if total_page > 0 and page <= total_page:
        row_start = (page - 1) * ROWS_PER_PAGE
        rows = total_rows.skip(row_start).limit(ROWS_PER_PAGE)

        for row in rows:
            page_info.rows.append(row)

    return render_template('search_normal_result.html',
                           title = "search_normal",
                           keywords = keywords,
                           page_info = page_info,
                           total_articles=total_page)

def save_personalinfo(datax):
    client = pymongo.MongoClient(host='localhost', port=27017)
    K_db = client.K_db
    collection = K_db.personalinfo
    datax["user_id"] = uuid.uuid1()
    global g_user_id
    g_user_id = datax["user_id"]
    #print(datax)
    collection.insert_one(datax).inserted_id

@app.route("/search_profession")
def search_profession():
    article_total_nums = 1000
    return render_template('search_profession.html',
        title = 'search_profession',
        total_articles = article_total_nums)

@app.route("/search_item")
def search_item():
    article_total_nums = 1000
    # SrcDatabase={{item['SrcDatabase-来源库']}}
    # &Title={{item['Title-题名']}}
    # &Author={{item['Author-作者']}}
    # &Organ={{item['Organ-单位']}}
    # &Source={{item['Source-文献来源']}}
    # &Keyword={{item['Keyword-关键词']}}
    # &Summary={{item['Summary-摘要']}}

    return render_template('search_item.html',
        srcDatabase_m=request.args.get('SrcDatabase'),
        title_m=request.args.get('Title'),
        author_m=request.args.get('Author'),
        organ_m=request.args.get('Organ'),
        source_m=request.args.get('Source'),
        keyword_m=request.args.get('Keyword'),
        summary_m=request.args.get('Summary'),
        title = 'Search Item',
        total_articles = article_total_nums)

@app.route("/search_normal_result_secondary")
def search_normal_result_secondary():
    user_id = request.args.get('user_id')
    keywords = request.args.get('keywords')

    page = int(request.args.get('page', 1))

    #save_personalSearchInfo(name, age, keywords)

    if page < 1:
        page = 1

    # get the total count and page:
    page_tmp = get_search_result(keywords, page)
    #kinds = get_search_result_kinds(page_tmp['rows'])

    page_info = getPageInfo()
    page_info.total_rows = page_tmp['rows']
    page_info.total_page = page_tmp['total_page']
    page_info.current_page = page_tmp['current']

    left_row = get_left_row(page_info)

    return render_template('search_normal_result_secondary.html',
                           title = "search_normal",
                           keywords = keywords,
                           page_info = page_info,
                           left_row = left_row,
                           total_articles=page_info.total_page)

@app.route("/end_search", methods = ["POST", "GET", "PUSH"])
def end_search():
    #user_id = request.form.get('user_id')
    #suggest = request.form.get('suggest')
    #print(str(user_id) +" :"+ str(suggest))
    return redirect("/index")

@app.route("/exit_view_first", methods = ["POST", "GET", "PUSH"])
def exit_view_first():
    article_total_nums = 1000
    user_id = request.form.get('user_id')

    # save question class search view 2

    return render_template('exit_view_first.html',
        title = 'exit_view',
        total_articles = article_total_nums,
        user_id = user_id)

@app.route("/exit_view_secondary", methods = ["POST", "GET", "PUSH"])
def exit_view_secondary():
    article_total_nums = 1000
    user_id = request.form.get('user_id')

    # save question class search view 2

    return render_template('exit_view_secondary.html',
        title = 'exit_view',
        total_articles = article_total_nums,
        user_id = user_id)

@app.route("/view_secondary_question", methods = ["POST", "GET", "PUSH"])
def view_secondary_question():
    article_total_nums = 1000
    user_id = request.args.get('user_id')
    #print('view_secondary_question start')
    save_personal_time_end(user_id)
    #print('view_secondary_question end')
    return render_template('view_secondary_question.html',
        title = 'view_secondary_question',
        total_articles = article_total_nums,
        user_id = user_id)

@app.route("/search_key_secondary")
def search_key_secondary():
    page = int(request.args.get('page', 1))
    if page < 1:
        page = 1

    doc_class = request.args.get('doc_class')
    key = request.args.get('keywords')
    page_tmp = get_search_result(key, page)
    user_id = request.args.get('user_id')

    page_info = getPageInfo()
    page_info.total_rows = page_tmp['rows']
    page_info.total_page = page_tmp['total_page']
    page_info.current_page = page_tmp['current']
    left_row = get_left_row(page_info)
    page_info = fix_page_info(page_info, doc_class)

    return render_template('search_key_secondary.html',
        keys=left_row,
        keywords=key,
        doc_class=doc_class,
        pages=page_info,
        title = 'Search Key Secondary',
        total_articles = 1,
        user_id = user_id)

@app.route("/search_normal_start_secondary", methods = ["POST", "GET", "PUSH"])
def search_normal_start_secondary():
    user_id = request.args.get('user_id')
    keywords = request.args.get('keywords')
    #print(keywords)
    #print(user_id)

    page_tmp = get_search_result(keywords, 1)

    page_info = getPageInfo()
    page_info.total_rows = page_tmp['rows']
    page_info.total_page = page_tmp['total_page']
    page_info.current_page = page_tmp['current']

    left_row = get_left_row(page_info)

    return render_template('search_normal_start_secondary.html',
                           title = "search normal start secondary",
                           keywords = keywords,
                           page_info = page_info,
                           left_row = left_row,
                           total_articles=page_info.total_page,
                           user_id = user_id)

@app.route("/search_secondary", methods = ["POST", "GET", "PUSH"])
def search_secondary():
    article_total_nums = 1000
    user_id = request.args.get('user_id')
    return render_template('search_secondary.html',
        title = 'view_secondary',
        total_articles = article_total_nums,
        user_id = user_id)

@app.route("/view_secondary", methods = ["POST", "GET", "PUSH"])
def view_secondary():
    user_id = request.form.get("user_id")
    #print(user_id)
    article_total_nums = 1000

    # save question class search view 1
    optionsRadiosinline1 = request.form.get('optionsRadiosinline1')
    print(optionsRadiosinline1)

    return render_template('view_secondary.html',
        title = 'view_secondary',
        total_articles = article_total_nums,
        user_id = user_id)

@app.route("/view_first_question", methods = ["POST", "GET", "PUSH"])
def view_first_question():
    article_total_nums = 1000
    user_id = request.args.get('user_id')
    return render_template('view_first_question.html',
        title = 'view_first_question',
        total_articles = article_total_nums,
        user_id = user_id)

def fix_page_info(page_info, key):
    page_info_ret = getPageInfo()
    index = 0
    key = key.strip(' ')
    rows = []
    for item in page_info.total_rows :
        '''
        print(key)
        print(item['Keyword-关键词'])
        print(item['Title-题名'])
        print(item['Summary-摘要'])
        '''
        if key in item['Keyword-关键词'] :
            rows.append(item)
            index = index + 1
        elif key in item['Summary-摘要'] :
            rows.append(item)
            index = index + 1
        elif key in item['Title-题名'] :
            rows.append(item)
            index = index + 1
        elif key in item['Classifier-类别'] :
            rows.append(item)
            index = index + 1

    page_info_ret.total_rows = rows
    page_info_ret.total_page = index
    page_info_ret.current_page = page_info.current_page

    if page_info_ret.current_page > page_info_ret.total_page :
        page_info_ret.current_page = page_info_ret.total_page

    return page_info_ret

@app.route("/search_key")
def search_key():
    page = int(request.args.get('page', 1))
    if page < 1:
        page = 1

    doc_class = request.args.get('doc_class')
    key = request.args.get('keywords')
    page_tmp = get_search_result(key, page)
    user_id = request.args.get('user_id')

    page_info = getPageInfo()
    page_info.total_rows = page_tmp['rows']
    page_info.total_page = page_tmp['total_page']
    page_info.current_page = page_tmp['current']
    left_row = get_left_row(page_info)
    page_info = fix_page_info(page_info, doc_class)

    return render_template('search_key.html',
        keys=left_row,
        keywords=key,
        doc_class=doc_class,
        pages=page_info,
        title = 'Search Key',
        total_articles = 1,
        user_id = user_id)

@app.route("/search_normal_start", methods = ["POST", "GET", "PUSH"])
def search_normal_start():
    user_id = request.args.get('user_id')
    keywords = request.args.get('keywords')
    #print(keywords)
    #print(user_id)

    #print("search_normal_start start")
    save_personal_time_start(user_id)
    #print("search_normal_start end")

    page_tmp = get_search_result(keywords, 1)

    page_info = getPageInfo()
    page_info.total_rows = page_tmp['rows']
    page_info.total_page = page_tmp['total_page']
    page_info.current_page = page_tmp['current']

    left_row = get_left_row(page_info)

    return render_template('search_normal_start.html',
                           title = "search_normal",
                           keywords = keywords,
                           page_info = page_info,
                           left_row = left_row,
                           total_articles=page_info.total_page,
                           user_id = user_id)




########## normal

@app.route("/normal_view_secondary_question", methods = ["POST", "GET", "PUSH"])
def normal_view_secondary_question():
    article_total_nums = 1000
    user_id = request.args.get('user_id')
    #print('normal_view_secondary_question start')
    save_personal_time_end(user_id)
    #print('normal_view_secondary_question end')
    return render_template('normal_view_secondary_question.html',
        title = 'view_first_question',
        total_articles = article_total_nums,
        user_id = user_id)

@app.route("/normal_search_key_secondary", methods = ["POST", "GET", "PUSH"])
def normal_search_key_secondary():
    page = int(request.args.get('page', 1))
    if page < 1:
        page = 1

    key = request.args.get('keywords')
    page_tmp = get_search_result(key, page)
    user_id = request.args.get('user_id')

    page_info = getPageInfo()
    page_info.total_rows = page_tmp['rows']
    page_info.total_page = page_tmp['total_page']
    page_info.current_page = page_tmp['current']

    return render_template('normal_search_key_secondary.html',
        keywords=key,
        pages=page_info,
        title = 'Search Key',
        total_articles = 1,
        user_id = user_id)

@app.route("/search_normal_secondary", methods = ["POST", "GET", "PUSH"])
def search_normal_secondary():
    article_total_nums = 1000
    user_id = request.args.get('user_id')
    #save_personal_time_start(user_id)
    return render_template('normal_search_secondary.html',
        name = "datax['name']",
        age = "datax['age']",
        title = 'search',
        total_articles = article_total_nums,
        user_id = user_id)

@app.route("/normal_view_secondary", methods = ["POST", "GET", "PUSH"])
def normal_view_secondary():
    user_id = request.form.get("user_id")
    #print(user_id)
    article_total_nums = 1000

    # save question class search view 2


    return render_template('normal_view_secondary.html',
        title = 'view_secondary',
        total_articles = article_total_nums,
        user_id = user_id)

@app.route("/normal_view_first_question", methods = ["POST", "GET", "PUSH"])
def normal_view_first_question():
    article_total_nums = 1000
    user_id = request.args.get('user_id')
    return render_template('normal_view_first_question.html',
        title = 'view_first_question',
        total_articles = article_total_nums,
        user_id = user_id)

@app.route("/normal_search_key", methods = ["POST", "GET", "PUSH"])
def normal_search_key():
    page = int(request.args.get('page', 1))
    if page < 1:
        page = 1

    key = request.args.get('keywords')
    page_tmp = get_search_result(key, page)
    user_id = request.args.get('user_id')

    page_info = getPageInfo()
    page_info.total_rows = page_tmp['rows']
    page_info.total_page = page_tmp['total_page']
    page_info.current_page = page_tmp['current']

    return render_template('normal_search_key.html',
        keywords=key,
        pages=page_info,
        title = 'Search Key',
        total_articles = 1,
        user_id = user_id)

@app.route("/search_normal", methods = ["POST", "GET", "PUSH"])
def search_normal():
    article_total_nums = 1000
    user_id = request.args.get('user_id')
    #print("search_normal start")
    save_personal_time_start(user_id)
    #print("search_normal end")
    return render_template('normal_search_first.html',
        name = "datax['name']",
        age = "datax['age']",
        title = 'search',
        total_articles = article_total_nums,
        user_id = user_id)

@app.route("/search", methods = ["POST", "GET", "PUSH"])
def search():
    article_total_nums = 1000
    user_id = request.args.get('user_id')
    return render_template('search.html',
        name = "datax['name']",
        age = "datax['age']",
        title = 'search',
        total_articles = article_total_nums,
        user_id = user_id)

@app.route("/view_first_normal")
def view_first_normal():
    article_total_nums = 1000
    user_id = request.args.get('user_id')
    return render_template('view_first_normal.html',
        title = 'view_first_normal',
        total_articles = article_total_nums,
        user_id = user_id)

@app.route("/view_first")
def view_first():
    article_total_nums = 1000
    user_id = request.args.get('user_id')
    return render_template('view_first.html',
        title = 'view_first',
        total_articles = article_total_nums,
        user_id = user_id)

@app.route("/dispatch", methods = ["POST"])
def dispatch():
    datax = request.form.to_dict()

    '''
    #print(datax)

    global g_name
    global g_age
    g_name = "datax['name']"
    g_age  = "datax['age']"
    print(g_name)
    print(g_age)
    print(datax['name'])
    print(datax['age'])
    print(datax['sex'])
    print(datax['education'])
    print(datax['search_time'])
    print(datax['search_rate'])
    print(datax['search_kinds'])
    print(datax['search_path'])
    '''

    save_personalinfo(datax)
    #print(g_user_id)

    article_total_nums = 1000
    return render_template('dispatch.html',
        title = 'dispatch',
        total_articles = article_total_nums,
        user_id = g_user_id)

@app.route("/personalinfo", methods = ["GET"])
def personalinfo():
    article_total_nums = 1000
    return render_template('personalinfo.html',
        title = 'Personal Info',
        total_articles = article_total_nums)

@app.route("/check_input", methods = ["POST"])
def check_input():
    user_id = request.form.get('user_id')
    #print(user_id)
    check_args = request.form.get('check_args')
    args = [arg for arg in check_args.strip().split('breeve') if arg != '']
    #print(args)

    return 'ok'

@app.route("/")
@app.route("/index")
def index():
    global g_name
    global g_age
    g_name = ""
    g_age  = 0

    article_total_nums = 1000
    return render_template('index.html',
        title = 'Home',
        total_articles = article_total_nums)