#!/usr/bin/python
#coding=utf-8

import jieba.posseg as pseg
import codecs
from gensim import corpora, models, similarities


class file_item:
    g_srcDatabase_k = ''
    g_title_k = ''
    g_author_k = ''
    g_organ_k = ''
    g_source_k = ''
    g_keyword_k = ''
    g_summary_k = ''

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

    while 1:
        line = file_name.readline()
        if not line:
            break

        line_str = line.split(':')

        if line_str[0] == g_srcDatabase_k:
            item = file_item()
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
                items[len(items)-1].g_summary_k = items[len(items)-1].g_summary_k + line

    for item in items:
        print(item.title_k)

    return items


def run():
    # 读取已经分类文件
    # items_ok = read_file(open("/root/Kdb/data/classifier_deal/all.txt"))

    # 读取待分类文件
    items_wait = read_file(open("/root/Kdb/data/classifier_deal/wait_classifier.txt"))


if __name__ == "__main__":
    run()