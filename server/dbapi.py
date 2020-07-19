import ZODB, ZODB.FileStorage
import transaction

from BTrees.OOBTree import TreeSet, OOBTree, BTree

def open_conn(db = 'database.fs'):
    storage = ZODB.FileStorage.FileStorage(db)
    db = ZODB.DB(storage)
    conn = db.open()
    return conn



def add_dictionary(d, db = 'database.fs'):
    conn = open_conn(db)
    root = conn.root()

    if root.dictionaries == None:
        root.dictionaries = BTree()

    if root.dictionaries[d.title] == None:
        root.dictionaries[d.title] = d

    return root[d.title]

