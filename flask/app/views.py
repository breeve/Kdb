import pymongo
import re
import math
import uuid
import time
import xlrd
import xlwt
import openpyxl
import os
from flask import Flask, render_template, send_from_directory, request, jsonify
from flask import render_template, flash, redirect, request
from app import app
from .forms import LoginForm
from .page_info import pageInfo, searchNormalItem

from .page_info import getPageInfo

ROWS_PER_PAGE = 10

g_name = ""
g_age  = 0
g_user_id = 0

# class_first      1
# class_secondary  2
# normal_first     3
# normal_secondary 4

def save_question(form, user_id, classifier):
    line1 = form.get('line1')
    line2 = form.get('line2')
    line3 = form.get('line3')
    line4 = form.get('line4')
    line5 = form.get('line5')

    line6 = form.get('line6')
    line7 = form.get('line7')
    line8 = form.get('line8')
    line9 = form.get('line9')

    line10 = form.get('line10')
    line11 = form.get('line11')
    line12 = form.get('line12')

    line13 = form.get('line13')
    line14 = form.get('line14')

    line15 = form.get('line15')

    '''
    print(line1)
    print(line2)
    print(line3)
    print(line4)
    print(line5)

    print(line6)
    print(line7)
    print(line8)
    print(line9)

    print(line10)
    print(line11)
    print(line12)

    print(line13)
    print(line14)

    print(line15)
    '''

    '''
    print(mind)
    print(physical)
    print(time)
    print(satisfy)
    print(strive)
    print(frustration)
    '''

    client = pymongo.MongoClient(host='localhost', port=27017)
    kdb = client.K_db
    collection = 0

    # class_first      1
    # class_secondary  2
    # normal_first     3
    # normal_secondary 4

    if classifier == 1:
        collection = kdb.question_class_first
    elif classifier == 2:
        collection = kdb.question_class_secondary
    elif classifier == 3:
        collection = kdb.question_normal_first
    elif classifier == 4:
        collection = kdb.question_normal_secondary
    else:
        return

    keywords_regex = {}
    keywords_regex['user_id'] = user_id
    row = collection.find_one(keywords_regex)

    question = {}

    question['line1'] = line1
    question['line2'] = line2
    question['line3'] = line3
    question['line4'] = line4
    question['line5'] = line5

    question['line6'] = line6
    question['line7'] = line7
    question['line8'] = line8
    question['line9'] = line9

    question['line10'] = line10
    question['line11'] = line11
    question['line12'] = line12

    question['line13'] = line13
    question['line14'] = line14

    question['line15'] = line15

    question['user_id'] = user_id
    if form.get('mind'):
        mind        = form.get('mind')
    if form.get('physical'):
        physical    = form.get('physical')
    if form.get('time'):
        time        = form.get('time')
    if form.get('satisfy'):
        satisfy     = form.get('satisfy')
    if form.get('strive'):
        strive      = form.get('strive')
    if form.get('frustration'):
        frustration = form.get('frustration')



    print('mind' + str(mind))
    print('physical' + str(physical))
    print('time' + str(time))
    print('satisfy' + str(satisfy))
    print('strive' + str(strive))
    print('frustration' + str(frustration))

    question['mind'] = str(mind)
    question['physical'] = str(physical)
    question['time'] = str(time)
    question['satisfy'] = str(satisfy)
    question['strive'] = str(strive)
    question['frustration'] = str(frustration)

    if row :
        collection.update(row, question)
    else:
        collection.insert_one(question).inserted_id




def save_personal_time_start(user_id):
    start_time = time.localtime(time.time())
    #print(str(user_id)+" start_time: "+str(start_time))

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

    #print(datax)


def save_personal_time_end(user_id):
    end_time = time.localtime(time.time())
    #print(str(user_id)+" end_time: "+str(end_time))

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

    #print(datax)

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
    save_question(request.form, user_id, 2)

    return render_template('exit_view_first.html',
        title = 'exit_view',
        total_articles = article_total_nums,
        user_id = user_id)

@app.route("/exit_view_secondary", methods = ["POST", "GET", "PUSH"])
def exit_view_secondary():
    article_total_nums = 1000
    user_id = request.form.get('user_id')

    # save question class search view 2
    save_question(request.form, user_id, 4)

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

    save_question(request.form, user_id, 1)

    # save question class search view 1

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

    save_question(request.form, user_id, 3)

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

    client = pymongo.MongoClient(host='localhost', port=27017)
    kdb = client.K_db
    collection = kdb.user_check_args

    keywords_regex = {}
    keywords_regex['user_id'] = user_id
    row = collection.find_one(keywords_regex)

    check_args = {}
    check_args['user_id'] = user_id
    check_args['args'] = args

    if row :
        collection.update(row, check_args)
    else:
        collection.insert_one(check_args).inserted_id

    return 'ok'

@app.route("/export_result")
def export_result():
    if os.path.exists('/root/Kdb/flask/app/upload/2003.xls'):
        print('remove ./app/upload/2003.xls')
        os.remove('/root/Kdb/flask/app/upload/2003.xls')

    wb = xlwt.Workbook()

    client = pymongo.MongoClient(host='localhost', port=27017)
    K_db = client.K_db



    '''
    personalinfo
    {
	"_id": ObjectId("5c7e7dad02f52b1c4e6f6441"),
	"search_rate": "1-从不",
	"age": "18",
	"user_id": BinData(3, "D3PSnD9NEemNORPOXnnBIQ=="),
	"search_path": "1-从来没有",
	"sex": "男",
	"search_time": "半年以内",
	"name": "",
	"search_kinds": "没用过",
	"education": "高中"
    } 
    '''


    sheet = wb.add_sheet("个人信息表")
    collection = K_db.personalinfo
    rows = collection.find()

    value = ['用户id', '年龄', '性别', '教育背景', '检索频率', '检索经验', '使用过的数据库种类个数', '7点李克特量表']

    for i in range(0, len(value)):
        sheet.write(0, i, value[i])

    i = 1
    for item in rows:
        if item['user_id'] :
            sheet.write(i, 0, str(item['user_id']))

        if item['age'] :
            sheet.write(i, 1, str(item['age']))

        if item['sex'] :
            sheet.write(i, 2, str(item['sex']))

        if item['education'] :
            sheet.write(i, 3, str(item['education']))

        if item['search_rate'] :
            sheet.write(i, 4, str(item['search_rate']))

        if item['search_time'] :
            sheet.write(i, 5, str(item['search_time']))

        if item['search_kinds'] :
            sheet.write(i, 6, str(item['search_kinds']))

        if item['search_path'] :
            sheet.write(i, 7, str(item['search_path']))


        i += 1

    '''
    personalTime
    {
	"_id": ObjectId("5c7e7dba02f52b1c4e6f6443"),
	"start_time": [2019, 3, 5, 8, 46, 34, 1, 64, 0],
	"end_time": [2019, 3, 5, 8, 47, 26, 1, 64, 0],
	"user_id": "0f73d29c-3f4d-11e9-8d39-13ce5e79c121"
    }
    '''

    sheet = wb.add_sheet("搜索时间表")
    collection = K_db.personalTime
    rows = collection.find()

    value = ['用户id', '开始时间', '结束时间']

    for i in range(0, len(value)):
        sheet.write(0, i, value[i])

    i = 1
    for item in rows:
        print(item['user_id'])
        print(item['start_time'])
        print(item['end_time'])

        if item['user_id']:
            sheet.write(i, 0, str(item['user_id']))

        if item['start_time']:
            sheet.write(i, 1, str(item['start_time']))

        if item['end_time']:
            sheet.write(i, 2, str(item['end_time']))


        i += 1

    '''
    question_class_first
    {
	"_id": ObjectId("5c7e7de002f52b1c4e6f6449"),
	"line15": "strive",
	"line1": "mind",
	"line10": "satisfy",
	"line5": "mind",
	"line13": "satisfy",
	"line3": "mind",
	"line9": "physical",
	"line14": "frustration",
	"line4": "strive",
	"user_id": "0f73d29c-3f4d-11e9-8d39-13ce5e79c121",
	"line12": "frustration",
	"line7": "physical",
	"line8": "strive",
	"line2": "time",
	"line11": "time",
	"line6": "time"
    }

    mind        = form.get('mind')
    physical    = form.get('physical')
    time        = form.get('time')
    satisfy     = form.get('satisfy')
    strive      = form.get('strive')
    frustration = form.get('frustration')

    '''
    sheet = wb.add_sheet("问卷一结果")
    collection = K_db.question_class_first
    rows = collection.find()

    value = ['用户id',
             '心智需求vs体力需求',
             '心智需求vs时间需求',
             '心智需求vs满足',
             '心智需求vs努力',
             '心智需求vs挫折感',
             '体力需求vs时间需求',
             '体力需求vs满足',
             '体力需求vs努力',
             '体力需求vs挫折感',
             '时间需求vs满足',
             '时间需求vs努力',
             '时间需求vs挫折感',
             '满足vs努力',
             '满足vs挫折感',
             '努力vs挫折感',
             '心智需求',
             '体力需求',
             '时间需求',
             '满足',
             '努力',
             '挫折感'
             ]

    for i in range(0, len(value)):
        sheet.write(0, i, value[i])

    i = 1
    for item in rows:
        sheet.write(i, 0, str(item['user_id']))

        if item['line1']:
            sheet.write(i, 1, str(item['line1']))

        if item['line2']:
            sheet.write(i, 2, str(item['line2']))

        if item['line3']:
            sheet.write(i, 3, str(item['line3']))

        if item['line4']:
            sheet.write(i, 4, str(item['line4']))

        if item['line5']:
            sheet.write(i, 5, str(item['line5']))

        if item['line6']:
            sheet.write(i, 6, str(item['line6']))
        if item['line7']:
            sheet.write(i, 7, str(item['line7']))
        if item['line8']:
            sheet.write(i, 8, str(item['line8']))
        if item['line9']:
            sheet.write(i, 9, str(item['line9']))

        if item['line10']:
            sheet.write(i, 10, str(item['line10']))
        if item['line11']:
            sheet.write(i, 11, str(item['line11']))
        if item['line12']:
            sheet.write(i, 12, str(item['line12']))

        if item['line13']:
            sheet.write(i, 13, str(item['line13']))
        if item['line14']:
            sheet.write(i, 14, str(item['line14']))

        if item['line15']:
            sheet.write(i, 15, str(item['line15']))

        if item['mind']:
            sheet.write(i, 15, str(item['mind']))

        if item['physical']:
            sheet.write(i, 15, str(item['physical']))

        if item['time']:
            sheet.write(i, 15, str(item['time']))

        if item['satisfy']:
            sheet.write(i, 15, str(item['satisfy']))

        if item['strive']:
            sheet.write(i, 15, str(item['strive']))

        if item['frustration']:
            sheet.write(i, 15, str(item['frustration']))


        i += 1

    '''
    question_class_secondary
    {
	"_id": ObjectId("5c7e7e0802f52b1c4e6f644f"),
	"line15": "frustration",
	"line1": "physical",
	"line10": "time",
	"line5": "frustration",
	"line13": "strive",
	"line3": "satisfy",
	"line9": "frustration",
	"line14": "satisfy",
	"line4": "mind",
	"user_id": "0f73d29c-3f4d-11e9-8d39-13ce5e79c121",
	"line12": "time",
	"line7": "satisfy",
	"line8": "physical",
	"line2": "mind",
	"line11": "strive",
	"line6": "physical"
    }
    '''

    sheet = wb.add_sheet("问卷二结果")
    collection = K_db.question_class_secondary
    rows = collection.find()

    value = ['用户id',
             '心智需求vs体力需求',
             '心智需求vs时间需求',
             '心智需求vs满足',
             '心智需求vs努力',
             '心智需求vs挫折感',
             '体力需求vs时间需求',
             '体力需求vs满足',
             '体力需求vs努力',
             '体力需求vs挫折感',
             '时间需求vs满足',
             '时间需求vs努力',
             '时间需求vs挫折感',
             '满足vs努力',
             '满足vs挫折感',
             '努力vs挫折感',
             '心智需求',
             '体力需求',
             '时间需求',
             '满足',
             '努力',
             '挫折感'
             ]

    for i in range(0, len(value)):
        sheet.write(0, i, value[i])

    i = 1
    for item in rows:
        sheet.write(i, 0, str(item['user_id']))

        if item['line1']:
            sheet.write(i, 1, str(item['line1']))

        if item['line2']:
            sheet.write(i, 2, str(item['line2']))

        if item['line3']:
            sheet.write(i, 3, str(item['line3']))

        if item['line4']:
            sheet.write(i, 4, str(item['line4']))

        if item['line5']:
            sheet.write(i, 5, str(item['line5']))

        if item['line6']:
            sheet.write(i, 6, str(item['line6']))
        if item['line7']:
            sheet.write(i, 7, str(item['line7']))
        if item['line8']:
            sheet.write(i, 8, str(item['line8']))
        if item['line9']:
            sheet.write(i, 9, str(item['line9']))

        if item['line10']:
            sheet.write(i, 10, str(item['line10']))
        if item['line11']:
            sheet.write(i, 11, str(item['line11']))
        if item['line12']:
            sheet.write(i, 12, str(item['line12']))

        if item['line13']:
            sheet.write(i, 13, str(item['line13']))
        if item['line14']:
            sheet.write(i, 14, str(item['line14']))

        if item['line15']:
            sheet.write(i, 15, str(item['line15']))

        if item['mind']:
            sheet.write(i, 15, str(item['mind']))

        if item['physical']:
            sheet.write(i, 15, str(item['physical']))

        if item['time']:
            sheet.write(i, 15, str(item['time']))

        if item['satisfy']:
            sheet.write(i, 15, str(item['satisfy']))

        if item['strive']:
            sheet.write(i, 15, str(item['strive']))

        if item['frustration']:
            sheet.write(i, 15, str(item['frustration']))

        i += 1

    '''
    user_check_args
    {
	"_id": ObjectId("5c7e7e8f02f52b0cdd7a281c"),
	"args": ["情报学研究中理论应用的国际比较\n"],
	"user_id": "79edcd6c-3f4d-11e9-8f84-cd6a8ac7ae3a"
    }
    '''

    sheet = wb.add_sheet("文章选择表")
    collection = K_db.user_check_args
    rows = collection.find()

    value = ['用户id', '有用的文章']

    for i in range(0, len(value)):
        sheet.write(0, i, value[i])

    i = 1
    for item in rows:
        sheet.write(i, 0, str(item['user_id']))
        if item['args']:
            sheet.write(i, 1, str(item['args']))

        i += 1

    wb.save('/root/Kdb/flask/app/upload/2003.xls')


    return send_from_directory('./upload', '2003.xls', as_attachment=True)

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