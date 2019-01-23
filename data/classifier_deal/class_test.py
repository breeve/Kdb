#!/usr/bin/python

import jieba.posseg as pseg
import codecs
from gensim import corpora, models, similarities


stop_words = './stopwords.dat'
stopwords = codecs.open(stop_words,'r',encoding='utf8').readlines()
stopwords = [ w.strip() for w in stopwords ]

stop_flag = ['x', 'c', 'u','d', 'p', 't', 'uj', 'm', 'f', 'r']

def tokenization(filename):
    result = []
    with open(filename, 'r') as f:
        text = f.read()
        words = pseg.cut(text)
    for word, flag in words:
        if flag not in stop_flag and word not in stopwords:
            result.append(word)
    return result

filenames = [
	'./all.txt',
	'./all.txt'
]

corpus = []

for each in filenames:
	corpus.append(tokenization(each))

print len(corpus)

dictionary = corpora.Dictionary(corpus)
print dictionary

doc_vectors = [dictionary.doc2bow(text) for text in corpus]
print len(doc_vectors)
print doc_vectors

tfidf = models.TfidfModel(doc_vectors)
tfidf_vectors = tfidf[doc_vectors]

print len(tfidf_vectors)
print len(tfidf_vectors[0])

query = tokenization('./stopwords.dat')

query_bow = dictionary.doc2bow(query)

print len(query_bow)
print query_bow

index = similarities.MatrixSimilarity(tfidf_vectors)

sims = index[query_bow]
print list(enumerate(sims))