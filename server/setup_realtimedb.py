import os
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from redctf.settings import RDB_HOST, RDB_PORT, CTF_DB


#### Setting up the app database

def dbSetup():
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db_drop(CTF_DB).run(connection)
    except RqlRuntimeError:
        pass

    try:
        r.db_create(CTF_DB).run(connection)
        r.db(CTF_DB).table_create('challenges').run(connection)
        r.db(CTF_DB).table_create('categories').run(connection)
        r.db(CTF_DB).table_create('teams').run(connection)
        print('Database setup completed!')
    except RqlRuntimeError as e:
        print('Error during database setup: %s' % (e))
    finally:
        connection.close()

if __name__ == "__main__":
    dbSetup()
    