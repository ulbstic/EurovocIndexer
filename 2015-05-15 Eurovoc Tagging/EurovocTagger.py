#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os, csv, re, nltk
from nltk.stem.snowball import SnowballStemmer # il est disponible en de nobmreuses langues


#####################################################
####################################################
###################################################

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


def FolderListWithTerminaison(terminaison):
    DocList = []
    for doc in os.listdir():
        if re.search (r'.*\%s$' % terminaison,doc) != None:
            DocList.append(doc)
    return DocList

def FolderListToDic(List):
    Dic = {}
    # the input should be a list of file contained in a folder
    for FileName in List:
        print('importing', FileName, '...')
        with open("%s" % FileName, "r", encoding='utf8') as myfile:
            text = myfile.read()
        Dic[FileName]= text
    return Dic

def TokenCleaning(token, stemmer):
    token = token.lower()
    token = stemmer_en.stem(token)
    return token

def RegexFromTerm(term, stemmer):

    # Regex Opening
    ################
    regex = r"\b("

    # Adding terms to regex
    ########################
    tokensList = nltk.word_tokenize(term)
    # en cas de terme à un mot
    if len(tokensList) == 1: 
        for token in tokensList:
            regex += TokenCleaning(token, stemmer)
    # si c'est un terme multi-mot
    else: 
        decount = len(tokensList)
        for token in tokensList:
            decount = decount -1
            # ajout de l'entre-mots
            if decount != len(tokensList)-1:
                regex+= r'\w*\W\w*\W*'
            # ajout du token
            regex += TokenCleaning(token, stemmer)

    # Regex Closure
    ################
    regex += '''\w{0,5})(\W)'''
    
    return regex


#####################################################
####################################################
###################################################



# création d'un dictionnaire Eurovoc à partir du TSF

TsvFile = "eurovoc.tsv"

EurovocDic, EurovocReverseDic, URIList, ConceptList = TsvDicProcessing(TsvFile)

print('Eurovoc importated!')

#=====================

# déplacement de dossier

print('moving to corpus folder...')
os.chdir('corpus/')

# détection des TXT dans le dossier

DocList = FolderListWithTerminaison('.txt')

# stockage du contenu des documents dans un dictionnaire

DocumentDic = FolderListToDic(DocList)             

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

            # REGEX CREATION
            regex = RegexFromTerm(concept, stemmer_en)

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



    
