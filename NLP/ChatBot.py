import os
import pandas as pd
import nltk
from fuzzywuzzy import fuzz
import re
from random import shuffle

from MedBotProject.settings import BASE_DIR

from . import Responses

from ML.projectF import pred

# USER STATE
# STATE 0 = INTRODUCTION & WELCOME
# STATE 1 = SYMPTOMS
# STATE 2 = SYMPTOM CONFIRM
# STATE 3 = DIAGNOSIS & ASK FOR GOING AGAIN
# STATE 4 = THANKS & END

def getResponse(symp_list):
    prediction = pred(symp_list)
    disease = prediction[0]
    precautions = prediction[1:]
    shuffle(Responses.DIAGNOSIS)
    shuffle(Responses.PRECAUTION)
    shuffle(Responses.THANK_YOU)
    diag_msg = Responses.DIAGNOSIS[0].format(disease)
    prec_list_msg = ''
    i=1
    for precaution in precautions:
        prec_list_msg = prec_list_msg + str(i) + '. ' + precaution + '\n'
        i+=1
    prec_msg = Responses.PRECAUTION[0].format(prec_list_msg)
    return diag_msg, prec_msg, Responses.THANK_YOU[0]

def welcome():
    shuffle(Responses.GREETINGS)
    return Responses.GREETINGS[0]

def getSymptoms(user_msg):
    # nltk.download('punkt')
    fpath = os.path.join(BASE_DIR, 'NLP', 'symptom-list.csv')
    df = pd.read_csv(fpath)
    STEMMED_SYMPTOMS = list(df['0'])
    SPACED_SYMPTOMS = list(df['1'])
    SYMPTOMS = list(df['2'])
    # print(SYMPTOMS)
    modified_user_msg = ''
    snow_stemmer = nltk.stem.SnowballStemmer('english')
    sentences = nltk.tokenize.sent_tokenize(user_msg)
    # print(sentences)
    for sentence in sentences:
        cleaned = re.sub(r'\'\w|[.,;:!-_\'\"]', '', sentence.lower())
        words = nltk.tokenize.word_tokenize(cleaned)
        new_sentence = ''
        for w in words:
            x = snow_stemmer.stem(w)
            new_sentence = new_sentence + x + ' '
        modified_user_msg += new_sentence
    modified_user_msg = modified_user_msg.strip()
    # print(modified_user_msg)
    user_symps = {}
    reject_symps = {}
    len_symp = len(SYMPTOMS)
    for i in range(len_symp):
        ratio = fuzz.token_set_ratio(modified_user_msg, STEMMED_SYMPTOMS[i])
        if ratio > 85:
            user_symps[STEMMED_SYMPTOMS[i]] = (ratio, SPACED_SYMPTOMS[i], SYMPTOMS[i])
        else:
            reject_symps[STEMMED_SYMPTOMS[i]] = (ratio, SPACED_SYMPTOMS[i], SYMPTOMS[i])
    # print(user_symp)
    # print(reject_symp)
    symp_items = list(user_symps.values())
    # print(symp_items)
    symp_list1 = list(s[1] for s in symp_items)
    symp_list2 = list(s[2] for s in symp_items)
    
    l = len(symp_list1)
    if l:
        symp_string = ''
        if l==1:
            symp_string = symp_list1[0]
        elif l==2:
            symp_string = symp_list1[0] + ' and ' + symp_list1[1]
        else:
            for i in range(l):
                if i == l-1:
                    symp_string = symp_string + 'and ' + symp_list1[i]
                elif i == l-2:
                    symp_string = symp_string + symp_list1[i] + ' '
                else:
                    symp_string = symp_string + symp_list1[i] + ', '
        shuffle(Responses.SYMPTOMS[1])
        bot_msg = Responses.SYMPTOMS[1][0].format(symp_string)
    else:
        shuffle(Responses.SYMPTOMS[0])
        bot_msg = Responses.SYMPTOMS[0][0]
    
    return bot_msg, symp_list2





def test():
    s = [
        'I am having frequent headaches. My muscles feel weak. Also having stiff movement.',
        'hehe',
    ]

    m, l = getSymptoms(s[0])
    print(m)
    print(l)
    if l:
        d, p, t = getResponse(l)
        print(d)
        print(p)
        print(t)
