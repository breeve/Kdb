#!/usr/bin/python

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

        if line_str[0] == g_g_srcDatabase_k:
            item = file_item()
            item.g_srcDatabase_k = line_str[1]
            key_tag = g_srcDatabase_k
        elif line_str[0] == g_title_k:
            item.g_title_k = line_str[1]
            key_tag = g_title_k
        elif line_str[0] == g_author_k:
            item.g_author_k = line_str[1]
            key_tag = g_author_k
        elif line_str[0] == g_organ_k:
            item.g_organ_k = line_str[1]
            key_tag = g_organ_k
        elif line_str[0] == g_source_k:
            item.g_source_k = line_str[1]
            key_tag = g_source_k
        elif line_str[0] == g_keyword_k:
            item.g_keyword_k = line_str[1]
            key_tag = g_keyword_k
        elif line_str[0] == g_summary_k:
            item.g_summary_k = line_str[1]
            key_tag = g_summary_k
            items.append(item)
        else :
            if key_tag == g_srcDatabase_k:
                item.g_srcDatabase_k = item.g_srcDatabase_k + line
            elif key_tag == g_title_k:
                item.g_title_k = item.g_title_k + line
            elif key_tag == g_author_k:
                item.g_author_k = item.g_author_k + line
            elif key_tag == g_organ_k:
                item.g_organ_k = item.g_organ_k + line
            elif key_tag == g_source_k:
                item.g_source_k = item.g_source_k + line
            elif key_tag == g_keyword_k:
                item.g_keyword_k = item.g_keyword_k + line
            elif key_tag == g_summary_k:
                items[len(items)-1].g_summary_k = items[len(items)-1].g_summary_k + line

    for item in items:
        print(item.title_k)


def run():
    # 读取待分类文件
    read_file("./all.txt")

    # 读取分类文件


if __name__ == "__main__":
    run