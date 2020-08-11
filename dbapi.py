import ZODB
import ZODB.FileStorage
import persistent.list
import persistent.mapping
import persistent
import transaction
from nltk.corpus import wordnet as wn, cmudict

cmudict_words = cmudict.words()


class Word(persistent.Persistent):
    def __init__(self, name):
        synset = wn.synsets(name)
        self.not_defined = False
        if len(synset) != 0:
            self.name, self.pos = synset[0].name().split('.')[0:2]
            self.synonyms = {a.name(): (a.definition(), a.examples()) for a in synset}
        elif name in cmudict_words:
            self.name = name
            self.not_defined = True
        else:
            self.not_defined = True
            return
        self.pronunciation = ' '.join([a for a in cmudict.entries()[cmudict_words.index(name)][1]])
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


def add_words(text):
    import os.path
    if not os.path.isfile('words.fs'):
        start_db()

    from nltk.corpus import stopwords
    from textblob import TextBlob
    sw = stopwords.words('english')

    words = [w for w in TextBlob(text).words if w not in sw]
    for word in words:
        add_word(word)
    return 1


def add_word(word, in_memory=None):
    storage = ZODB.FileStorage.FileStorage('words.fs')
    db = ZODB.DB(storage)
    conn = db.open()
    root = conn.root()
    try:
        rt = root['words']
        if word in rt:
            rt[word].count += 1
        else:
            rt[word] = Word(word)
    except:
        pass
    finally:
        transaction.commit()
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
                yield words[a].name, words[a].count
        except KeyError:
            return None
        # yield words
        finally:
            conn.close()
            db.close()


def start_db():
    storage = ZODB.FileStorage.FileStorage('words.fs')
    db = ZODB.DB(storage)
    conn = db.open()

    root = conn.root()
    root['words'] = persistent.mapping.PersistentMapping()
    transaction.commit()

    conn.close()
    db.close()

