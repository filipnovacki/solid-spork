import persistent
import transaction
from BTrees.OOBTree import TreeSet, OOBTree

from nltk.corpus import wordnet as wn
import cmudict

entries = cmudict.dict()


def define(word):
    wordsyn = wn.synsets(word)
    '''Couldn't find word'''
    if len(wordsyn) == 0:
        return
    out = {'pronunciation': [' '.join(a) for a in entries[word.split('.')[0]]],
           'syns': {a.name(): (a.definition(), a.examples()) for a in wordsyn}
           }
    transaction.commit()
    return out



class Dictionary(persistent.Persistent):
    def __init__(self, title):
        self.title = title
        self.words = OOBTree()

    def add_words(self, *words):
        for word in words:
            self.words.update({word: Word(word)})

    # Can't access object
    #def __repr__(self):
    #    return self.title



class Word(persistent.Persistent):
    def __init__(self, name):
        self.name = name
        self.not_defined = None

        # list of different pronunciations
        self.pronunciation = persistent.list.PersistentList()

        # synonyms and their exlpanations
        self.syns = OOBTree()

        if self.analyse() == 0:
            self.not_defined = True
        else:
            self.not_defined = False
        transaction.commit()

    def analyse(self):
        a = define(self.name)
        if a == None:
            return 0
        self.pronunciation = a['pronunciation']
        self.syns = OOBTree(a['syns'])
        transaction.commit()

    def __repr__(self):
        if self.not_defined == True:
            return self.name
        elif self.not_defined == False:
            # return the word and its synonyms
            return str(self.name + ': ' +
                       ', '.join(set([g.split('.')[0] for g in
                                      self.syns.keys()])))
        else:
            return self.name + ' (analysis not yet run)'

    def __eq__(self, other):
        if self.name == other.name:
            return True
        else:
            return False
