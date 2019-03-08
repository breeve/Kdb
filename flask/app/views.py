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
g_search_class = 1

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

    mind = 15
    physical = 25
    time = 45
    satisfy = 55
    strive = 35
    frustration = 75

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


    '''
    print('mind' + str(mind))
    print('physical' + str(physical))
    print('time' + str(time))
    print('satisfy' + str(satisfy))
    print('strive' + str(strive))
    print('frustration' + str(frustration))
    '''

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




def save_personal_time_start_first(user_id):
    user_id = str(user_id)
    start_time = time.time()
    #print(str(user_id)+" start_time: "+str(start_time))

    client = pymongo.MongoClient(host='localhost', port=27017)
    K_db = client.K_db
    collection = K_db.personalTime

    keywords_regex = {}
    keywords_regex['user_id'] = user_id
    row = collection.find_one(keywords_regex)

    datax = {}
    datax['user_id'] = user_id
    datax['start_time_first'] = start_time
    datax['end_time_first'] = 0
    datax['start_time_secondary'] = 0
    datax['end_time_secondary'] = 0

    if row :
        keys = row.keys()
        if 'end_time_first' in keys:
            datax['end_time_first'] = row['end_time_first']

        if 'start_time_secondary' in keys:
            datax['start_time_secondary'] = row['start_time_secondary']

        if 'end_time_secondary' in keys:
            datax['end_time_secondary'] = row['end_time_secondary']

        print (datax)
        collection.update(row, datax)
    else :
        print (datax)
        collection.insert_one(datax).inserted_id

    #print(datax)


def save_personal_time_end_first(user_id):
    user_id = str(user_id)
    end_time = time.time()
    #print(str(user_id)+" end_time: "+str(end_time))

    client = pymongo.MongoClient(host='localhost', port=27017)
    K_db = client.K_db
    collection = K_db.personalTime

    keywords_regex = {}
    keywords_regex['user_id'] = user_id
    row = collection.find_one(keywords_regex)

    datax = {}
    datax['user_id'] = user_id
    datax['start_time_first'] = 0
    datax['end_time_first'] = end_time
    datax['start_time_secondary'] = 0
    datax['end_time_secondary'] = 0
    if row is not None:
        keys = row.keys()
        if 'start_time_first' in keys:
            datax['start_time_first'] = row['start_time_first']

        if 'start_time_secondary' in keys:
            datax['start_time_secondary'] = row['start_time_secondary']

        if 'end_time_secondary' in keys:
            datax['end_time_secondary'] = row['end_time_secondary']
        print (datax)
        collection.update(row, datax)
    else :
        print (datax)
        collection.insert_one(datax).inserted_id

    save_personal_time_start_secondary(user_id)
    #print(datax)

def save_personal_time_start_secondary(user_id):
    user_id = str(user_id)
    start_time = time.time()
    #print(str(user_id)+" start_time: "+str(start_time))

    client = pymongo.MongoClient(host='localhost', port=27017)
    K_db = client.K_db
    collection = K_db.personalTime

    keywords_regex = {}
    keywords_regex['user_id'] = user_id
    row = collection.find_one(keywords_regex)

    datax = {}
    datax['user_id'] = user_id
    datax['start_time_first'] = 0
    datax['end_time_first'] = 0
    datax['start_time_secondary'] = start_time
    datax['end_time_secondary'] = 0

    if row is not None:
        keys = row.keys()
        if 'end_time_secondary' in keys:
            datax['end_time_secondary'] = row['end_time_secondary']

        if 'start_time_first' in keys:
            datax['start_time_first'] = row['start_time_first']

        if 'end_time_first' in keys:
            datax['end_time_first'] = row['end_time_first']

        print (datax)
        collection.update(row, datax)
    else :
        print (datax)
        collection.insert_one(datax).inserted_id

    #print(datax)


def save_personal_time_end_secondary(user_id):
    user_id = str(user_id)
    end_time = time.time()
    #print(str(user_id)+" end_time: "+str(end_time))

    client = pymongo.MongoClient(host='localhost', port=27017)
    K_db = client.K_db
    collection = K_db.personalTime

    keywords_regex = {}
    keywords_regex['user_id'] = user_id
    row = collection.find_one(keywords_regex)

    datax = {}
    datax['user_id'] = user_id
    datax['start_time_first'] = 0
    datax['end_time_first'] = 0
    datax['start_time_secondary'] = 0
    datax['end_time_secondary'] = end_time

    if row :
        keys = row.keys()

        if 'start_time_secondary' in keys:
            datax['start_time_secondary'] = row['start_time_secondary']

        if 'start_time_first' in keys:
            datax['start_time_first'] = row['start_time_first']

        if 'end_time_first' in keys:
            datax['end_time_first'] = row['end_time_first']

        print (datax)
        collection.update(row, datax)
    else :
        print (datax)
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

def save_task_select(user_id, task_select):
    client = pymongo.MongoClient(host='localhost', port=27017)
    K_db = client.K_db
    collection = K_db.taskSelect

    keywords_regex = {}
    keywords_regex['user_id'] = user_id
    row = collection.find_one(keywords_regex)

    datax = {}
    datax['user_id'] = user_id
    datax['task_select'] = task_select
    if row :
        collection.update(row, datax)
    else :
        collection.insert_one(datax).inserted_id

    #print(datax)

@app.route("/end_search", methods = ["POST", "GET", "PUSH"])
def end_search():
    user_id = request.form.get('user_id')
    task_select = request.form.get('task_select')

    save_task_select(user_id, task_select)
    return redirect("/index")

@app.route("/exit_view_first", methods = ["POST", "GET", "PUSH"])
def exit_view_first():
    article_total_nums = 1000
    user_id = request.form.get('user_id')

    # save question class search view 2
    save_question(request.form, user_id, 2)
    save_personal_time_end_secondary(user_id)

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
    save_personal_time_end_secondary(user_id)

    return render_template('exit_view_secondary.html',
        title = 'exit_view',
        total_articles = article_total_nums,
        user_id = user_id)

@app.route("/view_secondary_question", methods = ["POST", "GET", "PUSH"])
def view_secondary_question():
    article_total_nums = 1000
    user_id = request.args.get('user_id')
    #print('view_secondary_question start')
    #save_personal_time_end_secondary(user_id)
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
    #save_personal_time_start_secondary(user_id)

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
    save_personal_time_end_first(user_id)

    # save question class search view 1

    return render_template('view_secondary.html',
        title = 'view_secondary',
        total_articles = article_total_nums,
        user_id = user_id)

@app.route("/view_first_question", methods = ["POST", "GET", "PUSH"])
def view_first_question():
    article_total_nums = 1000
    user_id = request.args.get('user_id')
    #save_personal_time_end_first(user_id)
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
    #save_personal_time_end_secondary(user_id)
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
    #save_personal_time_start_secondary(user_id)
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
    save_personal_time_end_first(user_id)

    # save question class search view 2


    return render_template('normal_view_secondary.html',
        title = 'view_secondary',
        total_articles = article_total_nums,
        user_id = user_id)

@app.route("/normal_view_first_question", methods = ["POST", "GET", "PUSH"])
def normal_view_first_question():
    article_total_nums = 1000
    user_id = request.args.get('user_id')
    #save_personal_time_end_first(user_id)
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

    global g_search_class

    if g_search_class == 1:
        g_search_class = 2
    else:
        g_search_class = 1

    datax['search_class'] = g_search_class

    save_personalinfo(datax)
    #print(g_user_id)

    article_total_nums = 1000
    save_personal_time_start_first(datax["user_id"])
    if g_search_class == 1:
        return render_template('view_first.html',
                               title='view_first',
                               total_articles=article_total_nums,
                               user_id=g_user_id)

    return render_template('view_first_normal.html',
        title = 'view_first_normal',
        total_articles = article_total_nums,
        user_id = g_user_id)

@app.route("/personalinfo", methods = ["GET"])
def personalinfo():
    article_total_nums = 1000
    return render_template('personalinfo.html',
        title = 'Personal Info',
        total_articles = article_total_nums)

@app.route("/check_input_first", methods = ["POST"])
def check_input_first():
    user_id = request.form.get('user_id')
    #print(user_id)
    check_args = request.form.get('check_args')
    args = [arg for arg in check_args.strip().split('breeve') if arg != '']
    #print(args)

    client = pymongo.MongoClient(host='localhost', port=27017)
    kdb = client.K_db
    collection = kdb.user_check_args_view1

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

@app.route("/check_input_secondary", methods = ["POST"])
def check_input_secondary():
    user_id = request.form.get('user_id')
    #print(user_id)
    check_args = request.form.get('check_args')
    args = [arg for arg in check_args.strip().split('breeve') if arg != '']
    #print(args)

    client = pymongo.MongoClient(host='localhost', port=27017)
    kdb = client.K_db
    collection = kdb.user_check_args_view2

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


    user_id = 0

    sheet = wb.add_sheet("个人信息表")
    collection = K_db.personalinfo

    collection_personalTime = K_db.personalTime

    collection_question_class_first = K_db.question_class_first
    collection_question_class_secondary = K_db.question_class_secondary
    collection_question_normal_first = K_db.question_normal_first
    collection_question_normal_secondary = K_db.question_normal_secondary

    collection_user_check_args_view1 = K_db.user_check_args_view1
    collection_user_check_args_view2 = K_db.user_check_args_view2
    collection_taskSelect = K_db.taskSelect

    rows = collection.find()

    value = [
            '用户id', '搜索种类', '搜索经验高低', '任务难度选择',
            '年龄', '性别', '学历', '检索频率', '检索经验', '使用过的数据库种类个数', '7点李克特量表',

            '情景一文章', '情景一检索时间',
            '情景一Mind选择次数','情景一Physical选择次数','情景一Time选择次数',
            '情景一Eerformance选择次数','情景一Effort选择次数','情景一Frustration选择次数',
            '情景一Mind分数', '情景一Physical分数', '情景一Time分数',
            '情景一Eerformance分数', '情景一Effort分数', '情景一Frustration分数',

            '情景二文章', '情景二检索时间',
            '情景二Mind选择次数', '情景二Physical选择次数', '情景二Time选择次数',
            '情景二Eerformance选择次数', '情景二Effort选择次数', '情景二Frustration选择次数',
            '情景二Mind分数', '情景二Physical分数', '情景二Time分数',
            '情景二Eerformance分数', '情景二Effort分数', '情景二Frustration分数'
             ]

    for i in range(0, len(value)):
        sheet.write(0, i, value[i])

    i = 1
    for item in rows:
        #print(item.keys())
        keys = item.keys()
        if 'user_id' not in keys:
            continue

        if 'search_class' not in keys:
            continue

        if 'search_level' not in keys:
            continue

        if 'age' not in keys:
            continue

        if 'sex' not in keys:
            continue

        if 'education' not in keys:
            continue

        if 'search_rate' not in keys:
            continue

        if 'search_time' not in keys:
            continue

        if 'search_kinds' not in keys:
            continue

        if 'search_path' not in keys:
            continue


        user_id = str(item['user_id'])
        search_class = item['search_class']
        #print('search_class :' + str(search_class))
        search_cab = item['search_level']
        task_select = 1

        age = item['age']
        sex = item['sex'] # 男1 女2
        education = item['education']
        search_rate = item['search_rate']
        search_time = item['search_time']
        search_kinds = item['search_kinds']
        search_path = item['search_path']

        view1_args = ''
        view1_time = 0

        view1_mind_times = 0
        view1_physical_times = 0
        view1_time_times = 0
        view1_erformance_times = 0
        view1_effort_times = 0
        view1_frustration_times = 0

        view1_mind_score = 0
        view1_physical_score = 0
        view1_time_score = 0
        view1_erformance_score = 0
        view1_effort_score = 0
        view1_frustration_score = 0

        view2_args = ''
        view2_time = 0

        view2_mind_times = 0
        view2_physical_times = 0
        view2_time_times = 0
        view2_erformance_times = 0
        view2_effort_times = 0
        view2_frustration_times = 0

        view2_mind_score = 0
        view2_physical_score = 0
        view2_time_score = 0
        view2_erformance_score = 0
        view2_effort_score = 0
        view2_frustration_score = 0

        keywords_regex = {}
        keywords_regex['user_id'] = user_id

        # personalTime
        row_personal_time = collection_personalTime.find_one(keywords_regex)
        #print(row_personal_time)
        if row_personal_time is None:
            #print('row_personal_time None')
            continue

        keys = row_personal_time.keys()

        if 'start_time_first' not in keys:
            continue

        if 'end_time_first' not in keys:
            continue

        if 'start_time_secondary' not in keys:
            continue

        if 'end_time_secondary' not in keys:
            continue

        start_time_first = row_personal_time['start_time_first']
        end_time_first = row_personal_time['end_time_first']
        start_time_secondary = row_personal_time['start_time_secondary']
        end_time_secondary = row_personal_time['end_time_secondary']
        print(start_time_first)
        print(end_time_first)
        print(start_time_secondary)
        print(end_time_secondary)

        if end_time_first > start_time_first:
            view1_time = end_time_first - start_time_first
        else:
            view1_time = start_time_first - end_time_first

        if end_time_secondary > start_time_secondary:
            view2_time = end_time_secondary - start_time_secondary
        else:
            view2_time = start_time_secondary - end_time_secondary

        # user_check_args_view1
        row_user_check_args_view1 = collection_user_check_args_view1.find_one(keywords_regex)
        #print(row_user_check_args_view1)
        if row_user_check_args_view1 is None:
            print('row_user_check_args_view1 None')
        else:
            keys = row_user_check_args_view1.keys()

            if 'args' not in keys:
                continue

            view1_args = row_user_check_args_view1['args']

        # user_check_args_view2
        row_user_check_args_view2 = collection_user_check_args_view2.find_one(keywords_regex)
        #print(row_user_check_args_view2)
        if row_user_check_args_view2 is None:
            print('row_user_check_args_view2 None')
        else:
            keys = row_user_check_args_view2.keys()

            if 'args' not in keys:
                continue

            view2_args = row_user_check_args_view2['args']

        if search_class == 1:
            # question_class_first
            question_class_first = collection_question_class_first.find_one(keywords_regex)
            #print(question_class_first)
            if question_class_first is None:
                #print('question_class_first is None')
                continue

            keys = question_class_first.keys()

            if 'line1' not in keys:
                continue
            if 'line2' not in keys:
                continue
            if 'line3' not in keys:
                continue
            if 'line4' not in keys:
                continue
            if 'line5' not in keys:
                continue
            if 'line6' not in keys:
                continue
            if 'line7' not in keys:
                continue
            if 'line8' not in keys:
                continue
            if 'line9' not in keys:
                continue
            if 'line10' not in keys:
                continue
            if 'line11' not in keys:
                continue
            if 'line12' not in keys:
                continue
            if 'line13' not in keys:
                continue
            if 'line14' not in keys:
                continue
            if 'line15' not in keys:
                continue

            if 'mind' not in keys:
                continue
            if 'physical' not in keys:
                continue
            if 'time' not in keys:
                continue
            if 'satisfy' not in keys:
                continue
            if 'strive' not in keys:
                continue
            if 'frustration' not in keys:
                continue


            view1_mind_times = 0
            view1_physical_times = 0
            view1_time_times = 0
            view1_erformance_times = 0
            view1_effort_times = 0
            view1_frustration_times = 0

            if question_class_first['line1'] == 'mind':
                view1_mind_times += 1
            else:
                view1_physical_times += 1

            if question_class_first['line2'] == 'mind':
                view1_mind_times += 1
            else:
                view1_time_times += 1

            if question_class_first['line3'] == 'mind':
                view1_mind_times += 1
            else:
                view1_erformance_times += 1

            if question_class_first['line4'] == 'mind':
                view1_mind_times += 1
            else:
                view1_effort_times += 1

            if question_class_first['line5'] == 'mind':
                view1_mind_times += 1
            else:
                view1_frustration_times += 1


            if question_class_first['line6'] == 'physical':
                view1_physical_times += 1
            else:
                view1_time_times += 1

            if question_class_first['line7'] == 'physical':
                view1_physical_times += 1
            else:
                view1_erformance_times += 1

            if question_class_first['line8'] == 'physical':
                view1_physical_times += 1
            else:
                view1_effort_times += 1

            if question_class_first['line9'] == 'physical':
                view1_physical_times += 1
            else:
                view1_frustration_times += 1



            if question_class_first['line10'] == 'time':
                view1_time_times += 1
            else:
                view1_erformance_times += 1

            if question_class_first['line11'] == 'time':
                view1_time_times += 1
            else:
                view1_effort_times += 1

            if question_class_first['line12'] == 'time':
                view1_time_times += 1
            else:
                view1_frustration_times += 1


            if question_class_first['line13'] == 'satisfy':
                view1_erformance_times += 1
            else:
                view1_effort_times += 1

            if question_class_first['line14'] == 'satisfy':
                view1_erformance_times += 1
            else:
                view1_frustration_times += 1


            if question_class_first['line15'] == 'strive':
                view1_effort_times += 1
            else:
                view1_frustration_times += 1

            view1_mind_score = question_class_first['mind']
            view1_physical_score = question_class_first['physical']
            view1_time_score = question_class_first['time']
            view1_erformance_score = question_class_first['satisfy']
            view1_effort_score = question_class_first['strive']
            view1_frustration_score = question_class_first['frustration']


            # question_class_secondary
            question_class_secondary = collection_question_class_secondary.find_one(keywords_regex)
            #print(question_class_secondary)
            if question_class_secondary is None:
                #print('question_class_secondary is None')
                continue

            keys = question_class_secondary.keys()

            if 'line1' not in keys:
                continue
            if 'line2' not in keys:
                continue
            if 'line3' not in keys:
                continue
            if 'line4' not in keys:
                continue
            if 'line5' not in keys:
                continue
            if 'line6' not in keys:
                continue
            if 'line7' not in keys:
                continue
            if 'line8' not in keys:
                continue
            if 'line9' not in keys:
                continue
            if 'line10' not in keys:
                continue
            if 'line11' not in keys:
                continue
            if 'line12' not in keys:
                continue
            if 'line13' not in keys:
                continue
            if 'line14' not in keys:
                continue
            if 'line15' not in keys:
                continue

            if 'mind' not in keys:
                continue
            if 'physical' not in keys:
                continue
            if 'time' not in keys:
                continue
            if 'satisfy' not in keys:
                continue
            if 'strive' not in keys:
                continue
            if 'frustration' not in keys:
                continue

            view2_mind_times = 0
            view2_physical_times = 0
            view2_time_times = 0
            view2_erformance_times = 0
            view2_effort_times = 0
            view2_frustration_times = 0

            if question_class_secondary['line1'] == 'mind':
                view2_mind_times += 1
            else:
                view2_physical_times += 1

            if question_class_secondary['line2'] == 'mind':
                view2_mind_times += 1
            else:
                view2_time_times += 1

            if question_class_secondary['line3'] == 'mind':
                view2_mind_times += 1
            else:
                view2_erformance_times += 1

            if question_class_secondary['line4'] == 'mind':
                view2_mind_times += 1
            else:
                view2_effort_times += 1

            if question_class_secondary['line5'] == 'mind':
                view2_mind_times += 1
            else:
                view2_frustration_times += 1


            if question_class_secondary['line6'] == 'physical':
                view2_physical_times += 1
            else:
                view2_time_times += 1

            if question_class_secondary['line7'] == 'physical':
                view2_physical_times += 1
            else:
                view2_erformance_times += 1

            if question_class_secondary['line8'] == 'physical':
                view2_physical_times += 1
            else:
                view2_effort_times += 1

            if question_class_secondary['line9'] == 'physical':
                view2_physical_times += 1
            else:
                view2_frustration_times += 1



            if question_class_secondary['line10'] == 'time':
                view2_time_times += 1
            else:
                view2_erformance_times += 1

            if question_class_secondary['line11'] == 'time':
                view2_time_times += 1
            else:
                view2_effort_times += 1

            if question_class_secondary['line12'] == 'time':
                view2_time_times += 1
            else:
                view2_frustration_times += 1


            if question_class_secondary['line13'] == 'satisfy':
                view2_erformance_times += 1
            else:
                view2_effort_times += 1

            if question_class_secondary['line14'] == 'satisfy':
                view2_erformance_times += 1
            else:
                view2_frustration_times += 1


            if question_class_secondary['line15'] == 'strive':
                view2_effort_times += 1
            else:
                view2_frustration_times += 1

            view2_mind_score = question_class_secondary['mind']
            view2_physical_score = question_class_secondary['physical']
            view2_time_score = question_class_secondary['time']
            view2_erformance_score = question_class_secondary['satisfy']
            view2_effort_score = question_class_secondary['strive']
            view2_frustration_score = question_class_secondary['frustration']
        else:
            # question_normal_first
            question_normal_first = collection_question_normal_first.find_one(keywords_regex)
            #print(question_normal_first)
            if question_normal_first is None:
                #print('question_normal_first is None')
                continue
            keys = question_normal_first.keys()

            if 'line1' not in keys:
                continue
            if 'line2' not in keys:
                continue
            if 'line3' not in keys:
                continue
            if 'line4' not in keys:
                continue
            if 'line5' not in keys:
                continue
            if 'line6' not in keys:
                continue
            if 'line7' not in keys:
                continue
            if 'line8' not in keys:
                continue
            if 'line9' not in keys:
                continue
            if 'line10' not in keys:
                continue
            if 'line11' not in keys:
                continue
            if 'line12' not in keys:
                continue
            if 'line13' not in keys:
                continue
            if 'line14' not in keys:
                continue
            if 'line15' not in keys:
                continue

            if 'mind' not in keys:
                continue
            if 'physical' not in keys:
                continue
            if 'time' not in keys:
                continue
            if 'satisfy' not in keys:
                continue
            if 'strive' not in keys:
                continue
            if 'frustration' not in keys:
                continue
            view1_mind_times = 0
            view1_physical_times = 0
            view1_time_times = 0
            view1_erformance_times = 0
            view1_effort_times = 0
            view1_frustration_times = 0

            if question_normal_first['line1'] == 'mind':
                view1_mind_times += 1
            else:
                view1_physical_times += 1

            if question_normal_first['line2'] == 'mind':
                view1_mind_times += 1
            else:
                view1_time_times += 1

            if question_normal_first['line3'] == 'mind':
                view1_mind_times += 1
            else:
                view1_erformance_times += 1

            if question_normal_first['line4'] == 'mind':
                view1_mind_times += 1
            else:
                view1_effort_times += 1

            if question_normal_first['line5'] == 'mind':
                view1_mind_times += 1
            else:
                view1_frustration_times += 1

            if question_normal_first['line6'] == 'physical':
                view1_physical_times += 1
            else:
                view1_time_times += 1

            if question_normal_first['line7'] == 'physical':
                view1_physical_times += 1
            else:
                view1_erformance_times += 1

            if question_normal_first['line8'] == 'physical':
                view1_physical_times += 1
            else:
                view1_effort_times += 1

            if question_normal_first['line9'] == 'physical':
                view1_physical_times += 1
            else:
                view1_frustration_times += 1

            if question_normal_first['line10'] == 'time':
                view1_time_times += 1
            else:
                view1_erformance_times += 1

            if question_normal_first['line11'] == 'time':
                view1_time_times += 1
            else:
                view1_effort_times += 1

            if question_normal_first['line12'] == 'time':
                view1_time_times += 1
            else:
                view1_frustration_times += 1

            if question_normal_first['line13'] == 'satisfy':
                view1_erformance_times += 1
            else:
                view1_effort_times += 1

            if question_normal_first['line14'] == 'satisfy':
                view1_erformance_times += 1
            else:
                view1_frustration_times += 1

            if question_normal_first['line15'] == 'strive':
                view1_effort_times += 1
            else:
                view1_frustration_times += 1

            view1_mind_score = question_normal_first['mind']
            view1_physical_score = question_normal_first['physical']
            view1_time_score = question_normal_first['time']
            view1_erformance_score = question_normal_first['satisfy']
            view1_effort_score = question_normal_first['strive']
            view1_frustration_score = question_normal_first['frustration']


            # question_normal_secondary
            question_normal_secondary = collection_question_normal_secondary.find_one(keywords_regex)
            #print(question_normal_secondary)
            if question_normal_secondary is None:
                #print('question_normal_secondary is None')
                continue
            keys = question_normal_secondary.keys()

            if 'line1' not in keys:
                continue
            if 'line2' not in keys:
                continue
            if 'line3' not in keys:
                continue
            if 'line4' not in keys:
                continue
            if 'line5' not in keys:
                continue
            if 'line6' not in keys:
                continue
            if 'line7' not in keys:
                continue
            if 'line8' not in keys:
                continue
            if 'line9' not in keys:
                continue
            if 'line10' not in keys:
                continue
            if 'line11' not in keys:
                continue
            if 'line12' not in keys:
                continue
            if 'line13' not in keys:
                continue
            if 'line14' not in keys:
                continue
            if 'line15' not in keys:
                continue

            if 'mind' not in keys:
                continue
            if 'physical' not in keys:
                continue
            if 'time' not in keys:
                continue
            if 'satisfy' not in keys:
                continue
            if 'strive' not in keys:
                continue
            if 'frustration' not in keys:
                continue
            view2_mind_times = 0
            view2_physical_times = 0
            view2_time_times = 0
            view2_erformance_times = 0
            view2_effort_times = 0
            view2_frustration_times = 0

            if question_normal_secondary['line1'] == 'mind':
                view2_mind_times += 1
            else:
                view2_physical_times += 1

            if question_normal_secondary['line2'] == 'mind':
                view2_mind_times += 1
            else:
                view2_time_times += 1

            if question_normal_secondary['line3'] == 'mind':
                view2_mind_times += 1
            else:
                view2_erformance_times += 1

            if question_normal_secondary['line4'] == 'mind':
                view2_mind_times += 1
            else:
                view2_effort_times += 1

            if question_normal_secondary['line5'] == 'mind':
                view2_mind_times += 1
            else:
                view2_frustration_times += 1


            if question_normal_secondary['line6'] == 'physical':
                view2_physical_times += 1
            else:
                view2_time_times += 1

            if question_normal_secondary['line7'] == 'physical':
                view2_physical_times += 1
            else:
                view2_erformance_times += 1

            if question_normal_secondary['line8'] == 'physical':
                view2_physical_times += 1
            else:
                view2_effort_times += 1

            if question_normal_secondary['line9'] == 'physical':
                view2_physical_times += 1
            else:
                view2_frustration_times += 1



            if question_normal_secondary['line10'] == 'time':
                view2_time_times += 1
            else:
                view2_erformance_times += 1

            if question_normal_secondary['line11'] == 'time':
                view2_time_times += 1
            else:
                view2_effort_times += 1

            if question_normal_secondary['line12'] == 'time':
                view2_time_times += 1
            else:
                view2_frustration_times += 1


            if question_normal_secondary['line13'] == 'satisfy':
                view2_erformance_times += 1
            else:
                view2_effort_times += 1

            if question_normal_secondary['line14'] == 'satisfy':
                view2_erformance_times += 1
            else:
                view2_frustration_times += 1


            if question_normal_secondary['line15'] == 'strive':
                view2_effort_times += 1
            else:
                view2_frustration_times += 1

            view2_mind_score = question_normal_secondary['mind']
            view2_physical_score = question_normal_secondary['physical']
            view2_time_score = question_normal_secondary['time']
            view2_erformance_score = question_normal_secondary['satisfy']
            view2_effort_score = question_normal_secondary['strive']
            view2_frustration_score = question_normal_secondary['frustration']

        # taskSelect
        taskSelect = collection_taskSelect.find_one(keywords_regex)
        #print(taskSelect)
        if taskSelect is None:
            #print('taskSelect is None')
            continue
        keys = taskSelect.keys()

        if 'task_select' not in keys:
            continue
        task_select = taskSelect['task_select']


        sheet.write(i, 0, user_id)
        sheet.write(i, 1, search_class)
        sheet.write(i, 2, search_cab)
        sheet.write(i, 3, task_select)
        sheet.write(i, 4, age)
        sheet.write(i, 5, sex)
        sheet.write(i, 6, education)
        sheet.write(i, 7, search_rate)
        sheet.write(i, 8, search_time)
        sheet.write(i, 9, search_kinds)
        sheet.write(i, 10, search_path)
        sheet.write(i, 11, view1_args)
        sheet.write(i, 12, view1_time)
        sheet.write(i, 13, view1_mind_times)
        sheet.write(i, 14, view1_physical_times)
        sheet.write(i, 15, view1_time_times)
        sheet.write(i, 16, view1_erformance_times)
        sheet.write(i, 17, view1_effort_times)
        sheet.write(i, 18, view1_frustration_times)
        sheet.write(i, 19, view1_mind_score)
        sheet.write(i, 20, view1_physical_score)
        sheet.write(i, 21, view1_time_score)
        sheet.write(i, 22, view1_erformance_score)
        sheet.write(i, 23, view1_effort_score)
        sheet.write(i, 24, view1_frustration_score)
        sheet.write(i, 25, view2_args)
        sheet.write(i, 26, view2_time)
        sheet.write(i, 27, view2_mind_times)
        sheet.write(i, 28, view2_physical_times)
        sheet.write(i, 29, view2_time_times)
        sheet.write(i, 30, view2_erformance_times)
        sheet.write(i, 31, view2_effort_times)
        sheet.write(i, 32, view2_frustration_times)
        sheet.write(i, 33, view2_mind_score)
        sheet.write(i, 34, view2_physical_score)
        sheet.write(i, 35, view2_time_score)
        sheet.write(i, 36, view2_erformance_score)
        sheet.write(i, 37, view2_effort_score)
        sheet.write(i, 38, view2_frustration_score)
                       
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