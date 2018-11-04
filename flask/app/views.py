import pymongo
import re
import math
from flask import render_template, flash, redirect, request
from app import app
from .forms import LoginForm
from .page_info import pageInfo, searchNormalItem

from .page_info import getPageInfo

ROWS_PER_PAGE = 5

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


@app.route("/search_normal_result")
def search_normal_result():
    keywords = request.args.get('keywords')
    page = int(request.args.get('page', 1))

    if page < 1:
        page = 1

    # get the total count and page:
    page_tmp = get_search_result(keywords, page)

    page_info = getPageInfo()
    page_info.total_rows = page_tmp['rows']
    page_info.total_page = page_tmp['total_page']
    page_info.current_page = page_tmp['current']

    return render_template('search_normal_result.html',
                           title = "search_normal",
                           keywords = keywords,
                           page_info = page_info,
                           total_articles=page_info.total_page)

@app.route("/search_profession_result")
def search_profession_result():
    keywords = request.args.get('keywords')
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

@app.route("/search")
def search():
    article_total_nums = 1000
    return render_template('search.html',
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

@app.route("/")
@app.route("/index")
def index():
    article_total_nums = 1000
    return render_template('index.html',
        title = 'Home',
        total_articles = article_total_nums)