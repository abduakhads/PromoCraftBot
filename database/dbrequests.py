import sqlite3
import functools
from database import tables

con = sqlite3.connect("database/data.db")
con.isolation_level = None 

cur = con.cursor()
userslang = {}

def close_all_db():
    cur.close()
    con.close()

def transaction(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            cur.execute("BEGIN TRANSACTION")
            result = func(*args, **kwargs)
            cur.execute("COMMIT")
            return result
        except Exception as e:
            print("\n", func.__name__)
            print("\n\ndb/req Error:", e, "\n\n")
            con.rollback()
    return wrapper


@transaction
def setup_tables_db() -> bool:
    cur.execute(tables.users)
    cur.execute(tables.promos)
    cur.execute(tables.reflinks)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_reflinks_user_id ON reflinks (user_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_reflinks_promo_id ON reflinks (promo_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_promos_user_id ON promos (user_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_promos_channel_id ON promos (channel_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_promos_status ON promos (status)")
    return True


def load_ulangs_db() -> dict:
    cur.execute("SELECT user_id, lang FROM users")
    rows = cur.fetchall()
    result = {row[0]: row[1] for row in rows}
    del rows
    return result


@transaction
def upd_ulang_db(user_id: int, lang: str):
    cur.execute("UPDATE users SET lang = ? WHERE user_id = ?", (lang, user_id))


@transaction
def create_user_db(user_id: int, lang: str, fullname: str, username: str):
    cur.execute(
        "INSERT INTO users(user_id, lang, fullname, username) VALUES (?, ?, ?, ?)", 
        (user_id, lang, fullname, username)
    )





# if __name__ == "__main__":
#     setup_tables_db()
#     import pprint
#     pprint.pprint(fetch_user_langs())
#     cur.close()  # Closing the cursor
#     con.close()  # Closing the connection
