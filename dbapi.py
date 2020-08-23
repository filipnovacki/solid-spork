from ZODB import FileStorage, DB
import persistent.list
import persistent.mapping
import persistent
import transaction
from nltk.corpus import wordnet as wn, cmudict, stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

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
        print(" " if self.name == name else "x", "Word added: " + name + "\tO:" + self.name)

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


class WordsDB(object):
    def __init__(self, read_only=True):
        self.storage = FileStorage.FileStorage('words.fs', read_only=read_only)
        self.db = DB(self.storage)
        self.connection = self.db.open()
        self.dbroot = self.connection.root()

    def close(self):
        self.connection.close()
        self.db.close()
        self.storage.close()


def add_words(text, dictionary):
    sw = stopwords.words('english')

    words = [w for w in TextBlob(text).words if w not in sw]
    for word in words:
        if not str(word).isdigit():
            add_word(str(word), dictionary)


def add_word(word, dictionary, in_memory=None):
    vw = Word(word.lower())

    db = WordsDB(read_only=False)
    if dictionary not in db.dbroot:
        db.dbroot[dictionary] = persistent.mapping.PersistentMapping()
    rt = db.dbroot[dictionary]
    if word in rt:
        rt[word].count += 1
    elif not vw.not_defined:
        rt[word] = vw
    transaction.commit()
    db.close()


def get_words(dictionary):
    db = WordsDB()
    root = db.dbroot
    words = root[dictionary]
    for a in words:
        if not words[a].not_defined:
            yield words[a]
    db.close()


def get_word_names(dictionary):
    db = WordsDB()
    root = db.dbroot
    words = root[dictionary]
    for a in words:
        if not words[a].not_defined:
            yield words[a].name
    db.close()


def get_dicts_len():
    db = WordsDB()
    root = db.dbroot
    for dictionary in root:
        yield dictionary, len(root[dictionary])
    db.close()


def get_dicts():
    db = WordsDB()
    keys = db.dbroot.keys()
    db.close()
    return keys


def get_word_count(dictionary):
    db = WordsDB()
    root = db.dbroot
    root = root[dictionary]
    words = {'word': [],
             'count': []}
    for word in root:
        words['word'] += [root[word].name]
        words['count'] += [root[word].count]
    db.close()

    return words


def remove_dict(dictionary):
    db = WordsDB(read_only=False)
    root = db.dbroot
    if dictionary in root:
        del root[dictionary]
    transaction.commit()
    db.close()
