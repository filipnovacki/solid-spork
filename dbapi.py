import ZODB, ZODB.FileStorage
import transaction

from BTrees.OOBTree import TreeSet, OOBTree, BTree


def open_conn(db='database.fs'):
    """
    Opens connection to database

    db - path to database, defaults to database.fs. Optional argument
    returns open connection
    """
    storage = ZODB.FileStorage.FileStorage(db)
    db = ZODB.DB(storage)
    conn = db.open()
    return conn


def add_dictionary(d, db='database.fs'):
    """
    Adds dictionary to database.

    d - Dictionary class
    db - path to database. Defaults to database.fs. Optional argument

    returns added dictionary from the root object
    """
    conn = open_conn(db)
    root = conn.root()

    if root.dictionaries == None:
        root.dictionaries = BTree()

    if root.dictionaries[d.title] == None:
        root.dictionaries[d.title] = d

    return root[d.title]
