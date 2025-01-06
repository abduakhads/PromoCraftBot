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
    print("\nClosed db con and cur\n")

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
            # raise BaseException #adjust
    return wrapper


@transaction
def setup_tables_db() -> bool:
    cur.execute(tables.users)
    cur.execute(tables.promos)
    cur.execute(tables.reflinks)
    cur.execute(tables.subs)
    cur.execute(tables.channels)

    cur.execute("CREATE INDEX IF NOT EXISTS idx_reflinks_user_id ON reflinks (user_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_reflinks_promo_id ON reflinks (promo_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_reflinks_is_sub ON reflinks (is_sub)")

    cur.execute("CREATE INDEX IF NOT EXISTS idx_subs_user_id ON subs (user_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_subs_promo_id ON subs (promo_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_subs_is_sub ON subs (is_sub)")

    cur.execute("CREATE INDEX IF NOT EXISTS idx_promos_user_id ON promos (user_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_promos_channel_id ON promos (channel_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_promos_status ON promos (status)")
    
    cur.execute("CREATE INDEX IF NOT EXISTS idx_channels_user_id ON channels (user_id)")
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


def load_uchannels_db(user_id: int) -> list:
    cur.execute("SELECT channel_id, name, link FROM channels WHERE user_id = ?", (user_id,))
    return cur.fetchall()


@transaction
def insert_channel_db(channel_id: int, user_id: int, name: str, chlink: str):
    cur.execute(
        "INSERT OR REPLACE INTO channels(channel_id, user_id, name, link) VALUES (?, ?, ?, ?)",
        (channel_id, user_id, name, chlink)        
    )


@transaction
def remove_channel_db(channel_id: int):
    cur.execute(
        "DELETE FROM channels WHERE channel_id = ?",
        (channel_id,)        
    )


def get_usrby_channel_db(channel_id: int):
    cur.execute("SELECT user_id FROM channels WHERE channel_id = ?", (channel_id,))
    return cur.fetchall()


def get_channel_link_db(channel_id: int):
    cur.execute("SELECT link FROM channels WHERE channel_id = ?", (channel_id,))
    return cur.fetchall()


@transaction
def save_promo_db(
    user_id: int, channel_id: int, mode: str, title: str, 
    winner_count: int, expiration: str, member_limit: str
    ):
    cur.execute(
        "INSERT INTO promos(user_id, channel_id, mode, title, winner_count, expiration, memberlimit) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user_id, channel_id, mode, title, winner_count, expiration, member_limit)
    )


def get_upromos_db(user_id: int) -> list:
    cur.execute("SELECT promo_id, title FROM promos WHERE user_id = ? AND status = 1", (user_id,))
    return cur.fetchall()
