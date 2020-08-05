import ZODB
import ZODB.FileStorage
import persistent
import transaction
from nltk.corpus import wordnet as wn, cmudict


class Word(persistent.Persistent):
    def __init__(self, name):
        self.synset = wn.synsets(name)
        self.name, self.pos = self.synset[0].name().split('.')[0:2]
        self.not_defined = None
        self.synonyms = {a.name(): (a.definition(), a.examples()) for a in self.synset}
        self.pronunciation = ' '.join([a for a in cmudict.entries()[cmudict.words().index(name)][1]])

    def __repr__(self):
        if self.not_defined:
            return self.name
        elif not self.not_defined:
            return str(self.name + ': ' + ', '.join(set([g.split('.')[0] for g in self.synonyms.keys()])))
        else:
            return self.name + ' (analysis not yet run)'

    def __eq__(self, other):
        if self.name == other.name:
            return True
        else:
            return False


def add_dictionary(d, db='db/database.fs'):
    """
    Adds dictionary to database.

    d - Dictionary class
    db - path to database. Defaults to database.fs. Optional argument

    returns added dictionary from the root object
    """
    storage = ZODB.FileStorage.FileStorage(db)
    db = ZODB.DB(storage)
    conn = db.open()
    root = conn.root()

    root[d.title] = d

    transaction.commit()
    conn.close()
    db.close()

    return


def add_word(word, in_memory=None):
    if in_memory is not None:
        # write into database
        root = in_memory.root()
        try:
            root['words'] += [{word.name: word}]
        except KeyError:
            root['words'] = [{word.name: word}]
        transaction.commit()
        pass
    else:
        storage = ZODB.FileStorage.FileStorage('words.fs')
        db = ZODB.DB(storage)
        conn = db.open()
        root = conn.root()
        try:
            root['words'] += [{word.name: word}]
        except KeyError:
            root['words'] = [{word.name: word}]
        transaction.commit()
        db.close()

    return


def list_words(in_memory=None):
    if in_memory is not None:
        return in_memory['words']
    else:
        storage = ZODB.FileStorage.FileStorage('words.fs')
        db = ZODB.DB(storage)
        conn = db.open()
        root = conn.root()['words']
        db.close()
        return root
