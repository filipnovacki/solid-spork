import ZODB
import ZODB.FileStorage
import persistent.list
import persistent
import transaction
from nltk.corpus import wordnet as wn, cmudict


class Word(persistent.Persistent):
    def __init__(self, name):
        synset = wn.synsets(name)
        self.not_defined = False
        if len(synset) != 0:
            self.name, self.pos = synset[0].name().split('.')[0:2]
            self.synonyms = {a.name(): (a.definition(), a.examples()) for a in synset}
        elif name in cmudict.words():
            self.name = name
            self.not_defined = True
        else:
            self.not_defined = True
            return
        self.pronunciation = ' '.join([a for a in cmudict.entries()[cmudict.words().index(name)][1]])
        self.count = 1

    def __repr__(self):
        if self.not_defined:
            try:
                return self.name
            except AttributeError:
                return "Unknown word"
        elif not self.not_defined:
            return str(self.name + ': ' + ', '.join(set([g.split('.')[0] for g in self.synonyms.keys()])))
        else:
            return self.name + ' (analysis not yet run)'

    def __eq__(self, other):
        if self.name == other.name:
            return True
        else:
            return False


def add_word(word, in_memory=None):
    if in_memory is not None:
        # write into database
        root = in_memory.root()
        try:
            root['words'] += ({word.name: word},)
        except KeyError:
            root['words'] = ({word.name: word},)
        transaction.commit()
    else:
        vword = Word(word)
        storage = ZODB.FileStorage.FileStorage('words.fs')
        db = ZODB.DB(storage)
        conn = db.open()
        root = conn.root()
        rt = root['words']
        a = {word: vword}
        root['words'] = rt + [a]
        try:
            transaction.commit()
        except:
            return "Couldn't commit"
        finally:
            conn.close()
            db.close()


def list_words(in_memory=None):
    if in_memory is not None:
        return in_memory['words']
    else:
        storage = ZODB.FileStorage.FileStorage('words.fs')
        db = ZODB.DB(storage)
        conn = db.open()
        try:
            root = conn.root()
            words = root['words']
            for a in words:
                for x in a:
                    yield a[x].name
        except KeyError:
            return None
        # yield words
        conn.close()
        db.close()


def start_db():
    storage = ZODB.FileStorage.FileStorage('words.fs')
    db = ZODB.DB(storage)
    conn = db.open()

    root = conn.root()
    root['words'] = persistent.list.PersistentList()
    transaction.commit()

    conn.close()
    db.close()


# print(list(list_words()))
