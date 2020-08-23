import ZODB
import ZODB.FileStorage
import persistent.list
import persistent.mapping
import persistent
import transaction
from nltk.corpus import wordnet as wn, cmudict
from nltk.stem import WordNetLemmatizer

cmudict_words = cmudict.words()
ps = WordNetLemmatizer()


class Word(persistent.Persistent):
    def __init__(self, name):
        synset = wn.synsets(name)
        self.not_defined = False
        if len(synset) != 0:
            self.name = ps.lemmatize(name)
            self.pos = synset[0].name().split('.')[1]
            self.synonyms = {a.name(): (a.definition(), a.examples()) for a in synset}
        elif name in cmudict_words:
            self.name = ps.lemmatize(name)
            self.not_defined = True
            return
        else:
            self.not_defined = True
            return
        try:
            self.pronunciation = '-'.join([a for a in cmudict.entries()[cmudict_words.index(name)][1]])
            if type(self.pronunciation) is type([]):
                self.pronunciation = self.pronunciation[0]
        except:
            self.pronunciation = None
        self.count = 1
        print("t" if self.name == name else "f", "Word added: " + name, self.name)

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


def add_words(text, dictionary):
    from nltk.corpus import stopwords
    from textblob import TextBlob
    sw = stopwords.words('english')

    words = [w for w in TextBlob(text).words if w not in sw]
    for word in words:
        if not str(word).isdigit():
            add_word(str(word), dictionary)
    return 1


def add_word(word, dictionary, in_memory=None):
    vw = Word(word.lower())
    storage = ZODB.FileStorage.FileStorage('words.fs')
    db = ZODB.DB(storage)
    conn = db.open()
    root = conn.root()
    if dictionary not in root:
        root[dictionary] = persistent.mapping.PersistentMapping()
    rt = root[dictionary]
    if word in rt:
        rt[word].count += 1
    elif not vw.not_defined:
        rt[word] = vw
    transaction.commit()
    conn.close()
    db.close()


def get_words(dictionary):
    storage = ZODB.FileStorage.FileStorage('words.fs', read_only=True)
    db = ZODB.DB(storage)
    conn = db.open()
    root = conn.root()
    words = root[dictionary]
    for a in words:
        if not words[a].not_defined:
            yield words[a]
    conn.close()
    db.close()


def get_word_names(dictionary):
    storage = ZODB.FileStorage.FileStorage('words.fs', read_only=True)
    db = ZODB.DB(storage)
    conn = db.open()
    root = conn.root()
    words = root[dictionary]
    for a in words:
        if not words[a].not_defined:
            yield words[a].name
    conn.close()
    db.close()


def get_dicts_len():
    storage = ZODB.FileStorage.FileStorage('words.fs', read_only=True)
    db = ZODB.DB(storage)
    conn = db.open()
    root = conn.root()
    for dictionary in root:
        yield dictionary, len(root[dictionary])
    conn.close()
    db.close()


def start_db():
    storage = ZODB.FileStorage.FileStorage('words.fs')
    db = ZODB.DB(storage)
    db.close()


def get_dicts():
    storage = ZODB.FileStorage.FileStorage('words.fs', read_only=True)
    db = ZODB.DB(storage)
    conn = db.open()
    root = conn.root()
    for x in root:
        yield x
    conn.close()
    db.close()


def get_word_count(dictionary):
    storage = ZODB.FileStorage.FileStorage('words.fs', read_only=True)
    db = ZODB.DB(storage)
    conn = db.open()

    root = conn.root()
    if dictionary not in root:
        conn.close()
        db.close()
        return None
    root = root[dictionary]
    words = {'word': [],
             'count': []}
    for word in root:
        words['word'] += [root[word].name]
        words['count'] += [root[word].count]

    conn.close()
    db.close()

    return words

def remove_dict(dictionary):
    storage = ZODB.FileStorage.FileStorage('words.fs')
    db = ZODB.DB(storage)
    conn = db.open()
    root = conn.root()

    if dictionary in root:
        del root[dictionary]

    transaction.commit()

    conn.close()
    db.close()
