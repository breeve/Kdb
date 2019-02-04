# -*- coding: utf-8 -*-  
#!/usr/bin/python


import jieba.posseg as pseg
import codecs
import pymongo
from gensim import corpora, models, similarities


class file_item:
    index = 0
    srcDatabase_k = ''
    title_k = ''
    author_k = ''
    organ_k = ''
    source_k = ''
    keyword_k = ''
    summary_k = ''

class db_K_item:
    srcDatabase_k = ''
    title_k = ''
    author_k = ''
    organ_k = ''
    source_k = ''
    keyword_k = ''
    summary_k = ''

g_srcDatabase_k = "SrcDatabase-来源库"
g_title_k = "Title-题名"
g_author_k = "Author-作者"
g_organ_k = "Organ-单位"
g_source_k = "Source-文献来源"
g_keyword_k = "Keyword-关键词"
g_summary_k = "Summary-摘要"

def read_file(file_name):
    items = []
    item = file_item()
    key_tag = ''
    index = 0

    while 1:
        line = file_name.readline()
        if not line:
            break

        line_str = line.split(':')

        if line_str[0] == g_srcDatabase_k:
            item = file_item()
            item.index = index;
            index = index + 1
            item.srcDatabase_k = line_str[1]
            key_tag = g_srcDatabase_k
        elif line_str[0] == g_title_k:
            item.title_k = line_str[1]
            key_tag = g_title_k
        elif line_str[0] == g_author_k:
            item.author_k = line_str[1]
            key_tag = g_author_k
        elif line_str[0] == g_organ_k:
            item.organ_k = line_str[1]
            key_tag = g_organ_k
        elif line_str[0] == g_source_k:
            item.source_k = line_str[1]
            key_tag = g_source_k
        elif line_str[0] == g_keyword_k:
            item.keyword_k = line_str[1]
            key_tag = g_keyword_k
        elif line_str[0] == g_summary_k:
            item.summary_k = line_str[1]
            key_tag = g_summary_k
            items.append(item)
        else :
            if key_tag == g_srcDatabase_k:
                item.srcDatabase_k = item.srcDatabase_k + line
            elif key_tag == g_title_k:
                item.title_k = item.title_k + line
            elif key_tag == g_author_k:
                item.author_k = item.author_k + line
            elif key_tag == g_organ_k:
                item.organ_k = item.organ_k + line
            elif key_tag == g_source_k:
                item.source_k = item.source_k + line
            elif key_tag == g_keyword_k:
                item.keyword_k = item.keyword_k + line
            elif key_tag == g_summary_k:
                items[len(items)-1].summary_k = items[len(items)-1].summary_k + line

    for item in items:
        keys = item.keyword_k
        keys = keys.split(';')
        #print(keys[0])


    return items



def fils_class_create(items_ok):
    total = len(items_ok)
    file_classes = {}

    for item in items_ok :
        keys = item.keyword_k
        keys = keys.split(';')
        #print(item.index)
        for key in keys:
            key_final = key.split(',')
            for key in key_final :
                if len(key) == 0 :
                    continue
                #key = key.decode('utf-8')
                files = []

                if key in file_classes :
                    files = file_classes[key]

                files.append(item.index)

                file_classes[key] = files

    #for item in file_classes :
    #    print(file_classes[item])

    return file_classes

def insert_DB(collection, item):
    item_json = {
        "SrcDatabase-来源库":item.srcDatabase_k,
        "Title-题名":item.title_k,
        "Author-作者":item.author_k,
        "Organ-单位":item.organ_k,
        "Source-文献来源":item.source_k,
        "Keyword-关键词":item.keyword_k,
        "Summary-摘要":item.summary_k,
        "Classifier-类别":item.class_k
    }

    collection.insert_one(item_json).inserted_id
    return

def tokenization(text, stop_flag, stopwords):
    result = []
    words = pseg.cut(text)
    for word, flag in words:
        if flag not in stop_flag and word not in stopwords:
            result.append(word)
    return result

def run():
    # 读取已经分类文件
    items_ok = read_file(open("/root/Kdb/data/classifier_deal/all.txt"))
    #print(items_ok[0].keyword_k)

    # 读取待分类文件
    items_wait = read_file(open("/root/Kdb/data/classifier_deal/wait_classifier.txt"))

    # 构建已经分类的文章
    file_classes = fils_class_create(items_ok)
    for item in file_classes :
        index = file_classes[item][0]
        if index == 0 :
            print('-----------')
            print(item)
            print(file_classes[item])
            
            print(index)
            print(items_ok[index].title_k)
            print(items_ok[index].keyword_k)

    # 类别
    items = []
    item = db_K_item()

    # stop words
    stop_words = '/root/Kdb/data/classifier_deal/stopwords.dat'
    stopwords = codecs.open(stop_words,'r',encoding='utf8').readlines()
    stopwords = [ w.strip() for w in stopwords ]
    stop_flag = ['x', 'c', 'u','d', 'p', 't', 'uj', 'm', 'f', 'r']

    corpus = []
    for item in items_ok :
        corpus.append(tokenization(item.title_k+item.summary_k, stop_flag, stopwords))

    #print(len(corpus))

    # 建立词袋模型
    dictionary = corpora.Dictionary(corpus)
    #print(dictionary)

    doc_vectors = [dictionary.doc2bow(text) for text in corpus]
    #print(len(doc_vectors))
    #print(doc_vectors)

    tfidf = models.TfidfModel(doc_vectors)
    tfidf_vectors = tfidf[doc_vectors]
    #print(len(tfidf_vectors))
    #print(len(tfidf_vectors[0]))

    index = similarities.MatrixSimilarity(tfidf_vectors)

    # test
    query = tokenization(items_wait[0].title_k+items_wait[0].summary_k+items_wait[0].keyword_k,stop_flag, stopwords)
    query_bow = dictionary.doc2bow(query)
    #print(len(query_bow))
    #print(query_bow)

    sims = index[query_bow]
    #print(list(enumerate(sims)).sort())
    sims_list = list(enumerate(sims))
    sims_list = sorted(sims_list, key=lambda s: s[1])
    #print(sims_list[len(sims_list)-1])
    #最相似的
    sims_max = sims_list[len(sims_list)-1]

    #print(items_wait[0].title_k+items_wait[0].summary_k+items_wait[0].keyword_k)
    #print(sims_max[0])
    #print(sims_max[1])
    #print(items_ok[sims_max[0]].title_k+items_ok[sims_max[0]].summary_k+items_ok[sims_max[0]].keyword_k)

    # 存储到数据库
    client = pymongo.MongoClient(host='localhost', port=27017)
    K_db = client.K_db
    collection = K_db.maps_items
    
    srcDatabase_k = "SrcDatabase-来源库"
    title_k = "Title-题名"
    author_k = "Author-作者"
    organ_k = "Organ-单位"
    source_k = "Source-文献来源"
    keyword_k = "Keyword-关键词"
    summary_k = "Summary-摘要"
    classifier_k = "Classifier-类别"







if __name__ == "__main__":
    run()