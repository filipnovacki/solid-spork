import ZODB, ZODB.FileStorage
import transaction

from BTrees.OOBTree import TreeSet, OOBTree, BTree

def open_conn(db='db/database.fs'):
    """
    Opens connection to database

    db - path to database, defaults to database.fs. Optional argument
    returns open connection
    """
    storage = ZODB.FileStorage.FileStorage(db)
    db = ZODB.DB(storage)
    conn = db.open()
    return conn

# not used
def get_dictionaries(db='db/database.fs'):
    storage = ZODB.FileStorage.FileStorage(db)
    db = ZODB.DB(storage)
    conn = db.open()

    dicts = conn.root().items()
    conn.close()
    db.close()
    return dicts

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

# self.words.update({word: Word(word)})
