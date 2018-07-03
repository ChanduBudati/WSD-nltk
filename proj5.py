'''
Chandu Budati
CSCI 6350-001
Project #5
Due: 04/12/2018
File Description: This file contians all functions required to run WSD program, test sentences and word senses are in file input.txt
'''

import sys
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

'''
I tried different fetures and levels(sentence and word) to come up with sime thing.
It was hard to work with smaller sentences.

In wsd I compared the similarities of each word in the sentence to the one of the given sence, calculated the score for each sense based on the total similarity, Dint work as expected

In wsd2 I gathers some "noun" words form wordnet definations, examples, hyponym definations and examples and computed the max simlarity as score , results are as good as i expected but better than wsd
'''

#not using this method
def wsd(senses, sent, WORD):

    #word level features (similarity), Not very usefull
    stop_words = set(stopwords.words('english'))

    wlist = sent.split()
    wlist = [i.lower() for i in wlist if i.lower not in stop_words]
    wlist = [lemmatizer.lemmatize(i) for i in wlist]
    wlist = [i for i in wlist if i != WORD] #getting rid of actuall word as it would match with both senses anyway

    scoredict = {}
    for sense in senses.keys():
        score = 0
        #sense = wn.synset(s)
        for word in wlist:
            scoretemp = 0
            slist = wn.synsets(word)
            for ws in slist:
                sim = ws.wup_similarity(sense)
                if not sim:
                    continue
                if scoretemp < sim: # i am considering the maximum relevet sense of each word in the sentence
                    scoretemp = sim
            score += scoretemp
            #if score < scoretemp:
            #    score = scoretemp
        scoredict[senses[sense]] = score/wlist.__len__()

    return max(scoredict, key=scoredict.get)

#not using this method
def wsd1(senses, sents, word):
    worddict = {}
    for sense in senses.keys():
        words = []
        defi = sense.definition().split()

        defi = [lemmatizer.lemmatize(i, 'n') for i in defi if i.lower not in stop_words]

        words = words + defi
        exs = sense.examples()
        for ex in exs:
            words = words + ex.split()

        for w in defi:
            l = wn.synsets(w, 'n')
            if len(l) == 0:
                continue
            bs = l[0]
            sim = 0
            for le in l:
                tsim = le.wup_similarity(sense)
                if tsim:
                    if tsim > sim:
                        bs = le
                        sim = tsim
            if sim == 0:
                continue
            defi = bs.definition().split()
            defi = [lemmatizer.lemmatize(i, 'n') for i in defi if i.lower not in stop_words]
            words = words + defi

            exs = bs.examples()
            for ex in exs:
                words = words + [lemmatizer.lemmatize(i, 'n') for i in ex if i.lower not in stop_words]

        hypolist = sense.hyponyms()
        for h in hypolist:
            defi = h.definition().split()
            words = words + [lemmatizer.lemmatize(i, 'n') for i in defi if i.lower not in stop_words]
            exs = h.examples()
            for ex in exs:
                words = words+ [lemmatizer.lemmatize(i, 'n') for i in ex if i.lower not in stop_words]
        worddict[sense] = word

    for sense in worddict.keys():
        worddict[sense] = [lemmatizer.lemmatize(i, 'n') for i in worddict[sense] if i.lower not in stop_words]

    scoredict = {}
    sol = []
    for sent in sents:
        sent = sent.split()
        sent = [lemmatizer.lemmatize(i, 'n') for i in sent if i.lower not in stop_words]

        for sense in worddict.keys():
            score = 0
            for w in sent:
                if w in worddict[sense]:
                    score += 1
            scoredict[senses[sense]] = score
        sol.append(max(scoredict, key=scoredict.get))
    return sol

#utlility fun for wsd2
def getwords(sent):
    text = nltk.word_tokenize(sent)
    text = nltk.pos_tag(text)
    text = [lemmatizer.lemmatize(i[0]) for i in text if i[0].lower not in stop_words]# and 'NN' in i[1]]
    return text


#best apporach i could come up with
def wsd2(senses, sents, word):
    worddict = {}
    #creating a word list for all senses
    #nouns form defination and examples for sense, hyponym definations and examples
    for sense in senses.keys():
        words = []

        defi = sense.definition()
        words = words + getwords(defi) #getting lemmatized nouns

        exs = sense.examples()
        for ex in exs:
            words = words + getwords(ex)


        hypolist = sense.hyponyms()
        for h in hypolist:
            defi = h.definition()
            words = words + getwords(defi)

            exs = h.examples()
            for ex in exs:
                words = words + getwords(ex)
        worddict[sense] = words

    scoredict = {}
    sol = []
    for sent in sents:
        words = getwords(sent)

        #going throuh all words and finding max simliarity for each sense
        for sense in worddict.keys():
            score = 0
            for w in words:
                tscore = 0
                sim = 0
                bws = None
                for ws in wn.synsets(w):
                    tsim = ws.wup_similarity(sense)
                    if not tsim:
                        continue
                    if tsim > sim:
                        sim = tsim
                        bws = ws
                if not bws:
                    continue
                n = 0
                for dword in worddict[sense]:
                    sim = 0
                    dbws = None
                    for ws in wn.synsets(dword):
                        tsim = ws.wup_similarity(sense)
                        if not tsim:
                            continue
                        if tsim > sim:
                            sim = tsim
                            dbws = ws
                    if not dbws:
                        n += 1
                        continue
                    sim = bws.wup_similarity(dbws)
                    if sim != None:
                        if sim > tscore:
                            tscore = sim
                        #tscore += bws.wup_similarity(dbws)
                score = tscore/(len(worddict[sense]))
            scoredict[senses[sense]] = score
        sol.append(max(scoredict, key=scoredict.get)) #appendng results for all sentences into a list
    return sol

def main():
    #importing word senses and test data
    input = "input.txt"  # input("file address: ")
    file = open(input, 'r')
    testdata = file.readlines()
    file.close()

    testdata = [line.strip() for line in testdata ]


    word = lemmatizer.lemmatize(testdata[0].lower())

    #creating a dict of all the senses
    senses = {}
    senses[wn.synset(testdata[2])] = testdata[1]
    senses[wn.synset(testdata[4])] = testdata[3]

    sents = testdata[5:]

    #looping through all the test sents
    sol = wsd2(senses, sents, word)

    for i in range(len(sol)):
         print(sents[i]+" : " + sol[i])

    # for sent in sents:
    #     sol = wsd(senses, sent, word)
    #     print(sent + " (" + sol + ")")


main()