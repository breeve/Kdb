#! /usr/bin/python3

import pymongo

class db_K_item:
    srcDatabase_k = ''
    title_k = ''
    author_k = ''
    organ_k = ''
    source_k = ''
    keyword_k = ''
    summary_k = ''

def insert_DB(collection, item):
    item_json = {
        "SrcDatabase-来源库":item.srcDatabase_k,
        "Title-题名":item.title_k,
        "Author-作者":item.author_k,
        "Organ-单位":item.organ_k,
        "Source-文献来源":item.source_k,
        "Keyword-关键词":item.keyword_k,
        "Summary-摘要":item.summary_k
    }

    collection.insert_one(item_json).inserted_id
    return

def run(k_maps_file):
    client = pymongo.MongoClient(host='localhost', port=27017)
    K_db = client.K_db
    collection = K_db.maps_items

    items = []
    item = db_K_item()
    key_tag = ''

    srcDatabase_k = "SrcDatabase-来源库"
    title_k = "Title-题名"
    author_k = "Author-作者"
    organ_k = "Organ-单位"
    source_k = "Source-文献来源"
    keyword_k = "Keyword-关键词"
    summary_k = "Summary-摘要"

    while 1:
        line = k_maps_file.readline()
        if not line:
            break

        line_str = line.split(':')

        if line_str[0] == srcDatabase_k:
            item = db_K_item()
            item.srcDatabase_k = line_str[1]
            key_tag = srcDatabase_k
        elif line_str[0] == title_k:
            item.title_k = line_str[1]
            key_tag = title_k
        elif line_str[0] == author_k:
            item.author_k = line_str[1]
            key_tag = author_k
        elif line_str[0] == organ_k:
            item.organ_k = line_str[1]
            key_tag = organ_k
        elif line_str[0] == source_k:
            item.source_k = line_str[1]
            key_tag = source_k
        elif line_str[0] == keyword_k:
            item.keyword_k = line_str[1]
            key_tag = keyword_k
        elif line_str[0] == summary_k:
            item.summary_k = line_str[1]
            key_tag = summary_k
            items.append(item)
        else :
            if key_tag == srcDatabase_k:
                item.srcDatabase_k = item.srcDatabase_k + line
            elif key_tag == title_k:
                item.title_k = item.title_k + line
            elif key_tag == author_k:
                item.author_k = item.author_k + line
            elif key_tag == organ_k:
                item.organ_k = item.organ_k + line
            elif key_tag == source_k:
                item.source_k = item.source_k + line
            elif key_tag == keyword_k:
                item.keyword_k = item.keyword_k + line
            elif key_tag == summary_k:
                items[len(items)-1].summary_k = items[len(items)-1].summary_k + line

    for item in items:
        print(item.title_k)
        insert_DB(collection, item)

    print(len(items))
        


if __name__ == "__main__":
    k_maps_file = open("/root/Kdb/flask/datas/k_maps_489.txt")
    run(k_maps_file)
    k_maps_file = open("/root/Kdb/flask/datas/k_manager_1000.txt")
    run(k_maps_file)
