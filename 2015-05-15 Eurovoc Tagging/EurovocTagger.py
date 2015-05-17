#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os, csv, re, nltk
from nltk.stem.snowball import SnowballStemmer # il est disponible en de nobmreuses langues


#####################################################
####################################################
###################################################

def DicFromTsv(path):
    # !!! It only works with a 2 columns TSV file
    key = 0
    value = ""
    EurovocDic = {}
    with open(path, 'rt', encoding='utf8') as csvfile:
        myreader = csv.reader(csvfile, delimiter='\t')
        rcount = 0
        for row in myreader:
            rcount += 1
            ccount = 0
            if rcount > 1:
                for cells in row:
                    ccount += 1
                    if ccount ==1:
                        key = cells
                    else:
                        value = cells
                Dic[key] = value
    return Dic

def EurovocReverseDic(path):
    # !!! It only works with a 2 columns TSV file
    key = 0
    value = ""
    EurovocReverseDic = {}
    with open(path, 'rt', encoding='utf8') as csvfile:
        myreader = csv.reader(csvfile, delimiter='\t')
        rcount = 0
        for row in myreader:
            rcount += 1
            ccount = 0
            if rcount > 1:
                for cells in row:
                    ccount += 1
                    if ccount ==1:
                        key = cells
                    else:
                        value = cells
                EurovocReverseDic[value] = key
    return EurovocReverseDic

def TsvDicProcessing(path):
    # !!! It only works with a 2 columns TSV file
    Dic = {}
    RevDic = {}
    list1 = []
    list2 = []
    with open(path, 'rt', encoding='utf8') as csvfile:
        myreader = csv.reader(csvfile, delimiter='\t')
        rcount = 0
        for row in myreader:
            rcount += 1
            ccount = 0
            if rcount > 1:
                for cells in row:
                    ccount += 1
                    if ccount ==1:
                        list1.append(cells)
                        key = cells
                    else:
                        list2.append(cells)
                        value = cells
                Dic[key] = value
                RevDic[value] = key
    return Dic, RevDic, list1, list2



#####################################################
####################################################
###################################################



# création d'un dictionnaire Eurovoc à partir du TSF

TsvFile = "eurovoc.tsv"

EurovocDic, EurovocReverseDic, URIList, ConceptList = TsvDicProcessing(TsvFile)

print('Eurovoc importated!')

#=====================

# création d'une liste avec le nom des documents

os.chdir('corpus/')
DocList = []

# filtrage
for doc in os.listdir():
    if re.search (r'.*\.txt$',doc) != None:
        DocList.append(doc)

print('moving to corpus folder...')
# stockage du contenu des documents dans un dictionnaire

DocumentDic = {}

for DocName in DocList:
    print('importing', DocName, '...')
    with open("%s" % DocName, "r", encoding='utf8') as myfile:
        text = myfile.read()
    DocumentDic[DocName]= text               

#=====================

# tagging by researching concept-regexed as a substring of the text

stemmer_en = SnowballStemmer("english")

for DocName in DocList:
    tagsList=[]
    taggedText = ""
    print('tagging', DocName,'...')
    text = DocumentDic[DocName]
    text = text.lower()
    taggedText = text


#  un tag de concept se fera avec une étoile (*), et l'identifiant avec un +
    
    for concept in ConceptList:
        if concept != "": # IMPORTANT POUR EVITER DE TAGGER TOUT

            ####################
            # REGEX CREATION   #
            ####################

            regex = r"\b("
            tokensList = nltk.word_tokenize(concept)
            if len(tokensList) == 1: # en cas de terme à un mot
                for token in tokensList:
                    token = token.lower()
                    token = stemmer_en.stem(token)
                    regex += token
            else: # si c'est un terme multi-mot
                decount = len(tokensList)
                for token in tokensList:
                    decount = decount -1
                    if decount != len(tokensList)-1:
                        regex+= r'\w*\W\w*\W*' # admet un spération de 0 è 5 mots
                    token = token.lower()
                    token = stemmer_en.stem(token)
                    regex += token
            regex += '''\w{0,5})(\W)''' # longueur minimale apres le stemme pour eviter P. ex. que sea avec son "se" devienne "selection"

            # Now the regex is done

            ####################
            # TEMPORARY TAGGING#
            ####################
            
            # des symboles sémantiquements neutres sont choisi pour éviter que les concepts d'eurovoc matchent les tags
            if re.search(regex, text) != None:
                tagsList.append(concept)
                subRegex = r""
                subRegex += r'''<:><,>'''
                subRegex += EurovocReverseDic[concept] # insertion de l'identifiant qui servira ensuite pour l'URL
                subRegex += r'''</,>\1</:>\2'''
                taggedText = re.sub(regex, subRegex, taggedText)
                   
    #############################
    # POST PROCESSING TO REPORT #
    # FINAL HYPERTEXT TAGGING   #
    #############################           

    # créer un nouveau fichier avec le fichier taggué
    file = open("%s_TAGGED.html" % DocName, "w", encoding='utf8')
    htmlReportText = re.sub(r'''<:><,>''', r'''<span style="background-color: #FFFF00"><a href="http://eurovoc.europa.eu/''', taggedText)
    htmlReportText = re.sub(r'''</,>''', r'''">''', htmlReportText)
    htmlReportText = re.sub(r'''</:>''', r'''</a></span>''', htmlReportText)
    file.write("<html><body>")
    file.write(htmlReportText)
    file.write("</body><html>")
    file.close()       

    print(len(tagsList), 'concepts found:', tagsList)
            

# imprimer un rapport HMTL avec 1 "main page" avec un tableau et puis une page par texte contenant le texte taggé + URL vers Eurovoc



    
