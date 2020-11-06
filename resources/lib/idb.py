import os
import request
import sqlite3

try:
    import xbmc
    import xbmcaddon

    _database = os.path.join(xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')), 'resources/data/drama.db')
except ImportError:
    _database = '../data/drama.db'

_connection = None


def connect():
    global _connection

    if _connection is None:
        _connection = sqlite3.connect(_database)


def close():
    global _connection

    if _connection is not None:
        _connection.commit()
        _connection.close()
        _connection = None


def create():
    _connection.execute('CREATE TABLE IF NOT EXISTS drama ('
                        'path TEXT PRIMARY KEY ON CONFLICT IGNORE, '
                        'poster TEXT, '
                        'title TEXT, '
                        'plot TEXT, '
                        'year INT)')

    cursor = _connection.execute('SELECT path FROM drama')
    result = {path for (path,) in cursor.fetchall()}

    for path in request.dramalist('/drama-list'):
        if path not in result:
            add(path)


def add(path):
    (poster, title, plot, year) = request.dramadetail(path)
    _connection.execute('INSERT INTO drama VALUES (?, ?, ?, ?, ?)', (path, poster, title, plot, year))
    return poster, {'title': title, 'plot': plot, 'year': year}


def fetchone(path):
    cursor = _connection.execute('SELECT poster, title, plot, year FROM drama WHERE path = ?', (path,))
    result = cursor.fetchone()

    if result is None:
        return add(path)
    else:
        (poster, title, plot, year) = result
        return poster, {'title': title, 'plot': plot, 'year': year}


def fetchall(paths):
    cursor = _connection.execute('SELECT * FROM drama WHERE path IN (%s)' % ', '.join('?' * len(paths)), paths)
    paths = set(paths)

    for (path, poster, title, plot, year) in cursor.fetchall():
        paths.discard(path)
        yield path, poster, {'title': title, 'plot': plot, 'year': year}

    for path in paths:
        (poster, info) = add(path)
        yield path, poster, info
