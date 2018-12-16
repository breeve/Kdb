import pymongo
import re
import math
from flask import render_template, flash, redirect, request
from app import app
from .forms import LoginForm
from .page_info import pageInfo, searchNormalItem

from .page_info import getPageInfo

ROWS_PER_PAGE = 10000

g_name = ""
g_age  = 0

@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login request for OpenId=' + form.openid.data)
        return redirect('/index')
    return render_template('login.html',
        title = 'Sign in',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

def get_search_regex(keywords):
    keywords_regex = {}
    kws = [ks for ks in keywords.strip().split(' ') if ks != '']

    if len(kws) > 0:
        reg_pattern = re.compile('|'.join(kws), re.IGNORECASE)
        keywords_regex['Summary-摘要'] = reg_pattern

    return keywords_regex

def get_search_result(keywords, page):
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['K_db']
    keywords_regex = get_search_regex(keywords)
    #keywords_regex = {'Summary-摘要':{'$regex':'.*'+keywords+'.*'}}
    collection = db['maps_items']

    total_rows = collection.find(keywords_regex).count()
    total_page = int(math.ceil(total_rows / (ROWS_PER_PAGE * 1.0)))
    page_info = {'current': page, 'total_page': total_page,
                 'total_rows': total_rows, 'rows': []}

    if total_page > 0 and page <= total_page:
        row_start = (page - 1) * ROWS_PER_PAGE
        cursors = collection.find(keywords_regex) \
            .skip(row_start).limit(ROWS_PER_PAGE)

        for c in cursors:
            page_info['rows'].append(c)            

    print(keywords_regex)
    print(page_info)

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

    for key in keyword:
        print(key)

def get_left_row(page_info):
    keys = []
    for item in page_info.total_rows:
        for key in item["Keyword-关键词"].split(';;'):
            keys.append(key.split('\n')[0])
    # print(list(set(keys)))

    

    return keys

@app.route("/search_normal_result")
def search_normal_result():
    keywords = request.args.get('keywords')
    name = g_name
    age = g_age
    print("name: " + str(name))
    print("age: " + str(age))
    print("keywords: " + keywords)
    page = int(request.args.get('page', 1))

    save_personalSearchInfo(name, age, keywords)

    if page < 1:
        page = 1

    # get the total count and page:
    page_tmp = get_search_result(keywords, page)
    kinds = get_search_result_kinds(page_tmp['rows'])

    page_info = getPageInfo()
    page_info.total_rows = page_tmp['rows']
    page_info.total_page = page_tmp['total_page']
    page_info.current_page = page_tmp['current']

    left_row = get_left_row(page_info)

    return render_template('search_normal_result.html',
                           title = "search_normal",
                           keywords = keywords,
                           page_info = page_info,
                           left_row = left_row,
                           total_articles=page_info.total_page)

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
    print(datax)
    client = pymongo.MongoClient(host='localhost', port=27017)
    K_db = client.K_db
    collection = K_db.personalinfo
    collection.insert_one(datax).inserted_id


@app.route("/search", methods = ["POST"])
def search():
    datax = request.form.to_dict()
    print(datax)

    # {'name': '11',
    #  'age': '11', 
    #  'sex': '男', #
    #  'education': '高中', 
    #  'search_time': '半年以内', 
    #  'search_rate': '1-从不', 
    #  'search_kinds': '没用过', 
    #  'search_path': '1-从来没有'}

    global g_name
    global g_age
    g_name = datax['name']
    g_age  = datax['age']
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

    save_personalinfo(datax)

    g_name = datax['name']
    g_age  = datax['age']

    article_total_nums = 1000
    return render_template('search.html',
        name = datax['name'],
        age = datax['age'],
        title = 'search',
        total_articles = article_total_nums)

@app.route("/search_profession")
def search_profession():
    article_total_nums = 1000
    return render_template('search_profession.html',
        title = 'search_profession',
        total_articles = article_total_nums)    

@app.route("/personalinfo")
def personalinfo():
    article_total_nums = 1000
    return render_template('personalinfo.html',
        title = 'Personal',
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

@app.route("/search_key")
def search_key():
    keywords = request.args.get('keys')
    key = request.args.get('key')

    keys_tmp = keywords[1:len(keywords)-1]
    keys_tmp = keys_tmp.split(',')
    keys = []
    for item in keys_tmp :
        item = item.remove('\'').remove(' ')
        keys.append(item)


    return render_template('search_key.html',
        keys=keys,
        key=key,
        title = 'Search Key',
        total_articles = 1)

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