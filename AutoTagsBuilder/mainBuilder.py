import sqlConnector
import preProcess
import nltk
import re
from nltk.stem.porter import *
import gensim
from gensim import models
import json
import pandas as pd

def merge_sort(ary):
    if len(ary) <= 1 : return ary
    num = int(len(ary)/2)
    left = merge_sort(ary[:num])
    right = merge_sort(ary[num:])
    return merge(left,right)

def merge(left,right):
    l,r = 0,0
    result = []
    while l<len(left) and r<len(right) :
        if left[l][1] > right[r][1]:
            result.append(left[l])
            l += 1
        else:
            result.append(right[r])
            r += 1
    result += left[l:]
    result += right[r:]
    return result

def loadDocs():
    stopSet = set(nltk.corpus.stopwords.words('english'))
    docsDict = sqlConnector.getNewsContent()
    titleList = []
    docsList = []
    for title in docsDict.keys():
        doc0 = title + ': ' + docsDict[title]
        doc1 = nltk.word_tokenize(doc0)
        doc2 = [w.lower() for w in doc1]
        doc3 = []
        for word in doc2:
            if re.search('^[a-z]+$', word):
                doc3.append(re.search('^[a-z]+$', word).group())
        doc4 = [w for w in doc3 if w not in stopSet]
        titleList.append(title)
        docsList.append(doc4)
    dictionary = gensim.corpora.Dictionary(docsList)
    print('Load docs finished')
    return titleList, docsList, dictionary

def docs2vecs(docs, dictionary):
    vecs = [dictionary.doc2bow(doc) for doc in docs]
    print('Compute vecs finished')
    return vecs

def buildTfIdf(corpus):
    tfIdf = models.TfidfModel(corpus)
    tfIdfVecs = [tfIdf[c] for c in corpus]
    print('Transform tf-ids finished')
    return tfIdf, tfIdfVecs

def main():
    titleList, docsList, dictionary = loadDocs()
    vecs = docs2vecs(docsList, dictionary)
    tfIdf, tfIdfVecs = buildTfIdf(vecs)
    for i in range(len(tfIdfVecs)):
        tfIdfVecs[i] = merge_sort(tfIdfVecs[i])

    numTags = 5
    tagDict = dict()
    for m in range(len(titleList)):
        tagDict.update({titleList[m]: []})
        for n in range(numTags):
            try:
                tagPair = (dictionary[tfIdfVecs[m][n][0]])
                tagDict[titleList[m]].append(tagPair)
            except:
                tagDict[titleList[m]].append('')
    tagDF = pd.DataFrame(tagDict)
    tagDF = tagDF.T
    tagDF.index.name = 'NewsTitle'
    tagDF.to_csv('sampleOutput.csv')
    print('Output saving finished')

if __name__ == '__main__':
    main()