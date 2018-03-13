#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################
###########SYNOPSIS############
###############################
#
# Auteur : Sotiria BAMPATZANI
#
# Date : 10/03/18
#
# But : création d'une matrice d'incidences à partir des phrases se trouvant dans un seul document
#
# Usage : python3 incmatrix.py
###############################

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

import os
import re
import spacy
import fr_core_news_sm
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer

def openFile(f):
    '''lecture d'un fichier'''
    fi = open(f, encoding='utf8')
    return fi

def normalizeFile(f):
    '''normalisation de base d'un fichier'''
    fnorm = f.read().replace('\n', '')
    fnorm = fnorm.rstrip()
    return fnorm

def tokenizeText(text, encoding='utf8'):
    '''tokenisation du texte'''
    text = text.replace("’", "'")
    text = text.replace('«', '"')
    text = text.replace('»', '"')
    tokens = nltk.word_tokenize(text)
    return tokens

def removeStopwords(text, encoding='utf8'):
    '''suppression des mots vides'''
    stopWords = set(nltk.corpus.stopwords.words('french'))
    tokens = tokenizeText(text)
    tokens = [w.lower() for w in tokens if w.isalpha()]
    filteredTokens = [word for word in tokens if not word in stopWords]
    filteredTokens = []
    for word in tokens:
        if word not in stopWords:
            filteredTokens.append(word)
    return filteredTokens

def LemmatizeWords(listWords):
    '''lemmatisation'''
    listLemmas = list()
    strWords = " ".join(str(word) for word in listWords)
    nlp = fr_core_news_sm.load()
    strLemmas = nlp(strWords)
    for frLemma in strLemmas:
        listLemmas.append(frLemma.lemma_)
    return listLemmas


if __name__ == "__main__":
    
    pathFile = "F:\M2 TAL\M2 S2\Recherche d'information\TPs\miniCorpus.txt"

    try:
        os.path.exists(pathFile)
    except EnvironmentError:
        print("Problem with the path")
    else:
        f = openFile(pathFile)
        fic = normalizeFile(f)
        fic = re.sub(r"D\d\s?:\s?\s?", "\n", fic)
        fic = re.sub(r"^\n", "", fic)
        listPhrases = list()
        for line in fic.splitlines():
            listPhrases.append(line)
        print((listPhrases)
        vec = CountVectorizer()
        X = vec.fit_transform(listPhrases)
        df = pd.DataFrame(X.toarray(), columns=vec.get_feature_names())
        print(df)