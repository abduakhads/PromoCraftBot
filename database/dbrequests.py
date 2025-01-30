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
    cur.execute(tables.joins)

    cur.execute("CREATE INDEX IF NOT EXISTS idx_joins_ref ON joins (reflink_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_joins ON joins (user_id, channel_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_reflinks_user_id ON reflinks (user_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_reflinks_promo_id ON reflinks (promo_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_reflinks_is_sub ON reflinks (is_sub)")

    cur.execute("CREATE INDEX IF NOT EXISTS idx_subs_user_id ON subs (user_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_subs_promo_id ON subs (promo_id)")

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
    userslang[user_id] = lang
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
    return cur.fetchone()


def get_channel_link_db(channel_id: int):
    cur.execute("SELECT link, name FROM channels WHERE channel_id = ?", (channel_id,))
    return cur.fetchall()


@transaction
def save_promo_db(
    user_id: int, channel_id: int, mode: str, title: str, 
    winner_count: int, expiration: str, member_limit: str
    ) -> int:
    cur.execute(
        "INSERT INTO promos(user_id, channel_id, mode, title, winner_count, expiration, memberlimit) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user_id, channel_id, mode, title, winner_count, expiration, member_limit)
    )
    return cur.lastrowid


def get_upromos_db(user_id: int) -> list:
    cur.execute("SELECT promo_id, title FROM promos WHERE user_id = ? AND status = 1", (user_id,))
    return cur.fetchall()


def get_utimdiff_db(user_id: int) -> str | None:
    cur.execute("SELECT timediff FROM users WHERE user_id = ?", (user_id,))
    return cur.fetchall()


@transaction
def upd_utimediff_db(user_id: int, timediff: str):
    cur.execute("UPDATE users SET timediff = ? WHERE user_id = ?", (timediff, user_id))


def get_promo(promo_id: int):
    cur.execute(
        "SELECT channel_id, mode, expiration, memberlimit, title, winner_count FROM promos WHERE status = 1 AND promo_id = ?", (promo_id,)
    )
    return cur.fetchone()


@transaction
def set_reflink(user_id: int, promo_id: int, link: str):
    cur.execute(
        "INSERT INTO reflinks(user_id, promo_id, link) VALUES (?, ?, ?)", (user_id, promo_id, link)
    )


def get_reflink(user_id: int, promo_id: int):
    cur.execute(
        "SELECT reflink_id, link FROM reflinks WHERE user_id = ? AND promo_id = ?", (user_id, promo_id)
    )
    return cur.fetchone()


@transaction
def insert_sub(user_id: int, promo_id: int):
    cur.execute(
        "INSERT INTO subs(user_id, promo_id) VALUES (?, ?)",
        (user_id, promo_id)        
    )


def get_sub(user_id: int, promo_id: int):
    cur.execute(
        "SELECT sub_id FROM subs WHERE user_id = ? AND promo_id = ?", (user_id, promo_id)
    )
    return cur.fetchone()


def get_user_byreflink(link: str):
    cur.execute(
        "SELECT user_id FROM reflinks WHERE link = ?", (link,)
    )


@transaction
def insert_join(reflink_id: int, user_id: int, channel_id: int):
    cur.execute(
        "INSERT INTO joins VALUES (?, ?, ?)", (reflink_id, user_id, channel_id)
    )


@transaction
def update_reflink_join(user_id: int, promo_id: int, join: int = 1):
    cur.execute(
        "UPDATE reflinks SET joins = joins + ? WHERE user_id = ? AND promo_id = ?", (join, user_id, promo_id)
    )
    cur.execute("SELECT reflink_id FROM reflinks WHERE user_id = ? AND promo_id = ?", (user_id, promo_id))
    return cur.fetchone()


@transaction
def del_join(user_id: int, channel_id: int):
    cur.execute("SELECT reflink_id FROM joins WHERE user_id = ? AND channel_id = ?", (user_id, channel_id))
    if res := cur.fetchone():
        cur.execute("DELETE FROM joins WHERE user_id = ? AND channel_id = ?", (user_id, channel_id))
        cur.execute("UPDATE reflinks SET joins = joins - 1 WHERE reflink_id = ?", (res[0],))

        cur.execute("SELECT user_id FROM reflinks WHERE reflink_id = ?", (res[0],))
        return cur.fetchone()


@transaction
def del_player(user_id: int, channel_id: int):
    cur.execute(
        "DELETE FROM subs WHERE user_id = ? AND promo_id IN (SELECT promo_id FROM promos WHERE channel_id = ?)", 
        (user_id, channel_id)
    )
    cur.execute(
        "UPDATE reflinks SET is_sub = 0 WHERE user_id = ? AND promo_id IN (SELECT promo_id FROM promos WHERE channel_id = ?)",
        (user_id, channel_id)
    )
    # cur.execute(
    #     "SELECT link FROM reflinks WHERE user_id = ? AND promo_id IN (SELECT promo_id FROM promos WHERE channel_id = ?)", 
    #     (user_id, channel_id)
    # )
    # res = cur.fetchall()
    # cur.execute(
    #     "DELETE FROM reflinks WHERE user_id = ? AND promo_id IN (SELECT promo_id FROM promos WHERE channel_id = ?)",
    #     (user_id, channel_id)
    # )
    # return res

@transaction
def joined_back(user_id, channel_id):
    cur.execute(
        "UPDATE reflinks SET is_sub = 1 WHERE user_id = ? AND promo_id IN (SELECT promo_id FROM promos WHERE channel_id = ?)",
        (user_id, channel_id)
    )
    # cur.execute(
    #     "UPDATE reflinks SET joins = joins + 1 WHERE reflink_id IN (SELECT reflink_id FROM joins WHERE user_id = ? AND channel_id = ?)",
    #     (user_id, channel_id)
    # )


def get_reflinks(user_id: int):
    cur.execute(
        "SELECT p.title, ref.link, ref.joins FROM reflinks ref JOIN promos p ON ref.promo_id = p.promo_id WHERE ref.user_id = ?", (user_id,)
    )
    return cur.fetchall()


@transaction
def get_ready_promos(datetime):
    cur.execute(
        "UPDATE promos SET status = 0 WHERE promo_id IN (SELECT promo_id FROM promos WHERE expiration <= ? AND status = 1) RETURNING *", 
        (datetime,)
    )
    return cur.fetchall()


@transaction
def get_players(promo_id: int, joins: int | None, winners: int, mode: str):
    if joins and mode == "ref":
        cur.execute(
            "SELECT user_id FROM reflinks WHERE is_sub = 1 AND promo_id = ? AND joins = ? ORDER BY random() LIMIT ?",
            (promo_id, joins, winners)
        )
    elif mode == "ref":
        cur.execute(
            "SELECT user_id, joins FROM reflinks WHERE is_sub = 1 AND joins > 0 AND promo_id = ? ORDER BY joins DESC, reflink_id ASC LIMIT ?",
            (promo_id, winners)
        )
    elif mode == "sub":
        cur.execute(
            "SELECT user_id FROM subs WHERE promo_id = ? ORDER BY random() LIMIT ?",
            (promo_id, winners)
        )
    res = cur.fetchall()
    if res:
        return [row[0] for row in res] if joins or mode == "sub" else {row[0]: row[1] for row in res}
    return None


def get_users(uids: list):
    cur.execute(
        f"SELECT * FROM users WHERE user_id IN ({', '.join(['?'] * len(uids))})",
        tuple(uids)
    )
    return cur.fetchall()


def check_winners(promo_id: int):
    cur.execute("SELECT winners FROM promos WHERE promo_id = ?", (promo_id,))
    return cur.fetchone()


@transaction
def save_winners(promo_id: int, mess_id: int):
    cur.execute("UPDATE promos SET winners = ? WHERE promo_id = ?", (mess_id, promo_id))


@transaction
def get_participants_count(promo_id: int, mode: str, delete: bool = False):
    if mode == "ref":
        cur.execute("SELECT COUNT(*) FROM reflinks WHERE promo_id = ?", (promo_id,))
        res = cur.fetchone()
        if delete:
            cur.execute("DELETE FROM reflinks WHERE promo_id = ?", (promo_id,))
    elif mode == "sub":
        cur.execute("SELECT COUNT(*) FROM subs WHERE promo_id = ?", (promo_id,))
        res = cur.fetchone()
        if delete:
            cur.execute("DELETE FROM subs WHERE promo_id = ?", (promo_id,))
    return res


@transaction
def get_joins_count(promo_id: int, delete: bool = False):
    cur.execute("SELECT reflink_id FROM reflinks WHERE promo_id = ?", (promo_id,))
    res = cur.fetchall()
    reflink_ids = [row[0] for row in res]
    cur.execute(
            f"SELECT COUNT(*) FROM joins WHERE reflink_id IN ({', '.join(['?'] * len(reflink_ids))})",
            tuple(reflink_ids)
        )
    res = cur.fetchone()
    if delete:
        cur.execute(
            f"DELETE FROM joins WHERE reflink_id IN ({', '.join(['?'] * len(reflink_ids))})",
            tuple(reflink_ids)
        )
    return res


def get_reflinks_torevoke(promo_id):
    cur.execute("SELECT link FROM reflinks WHERE promo_id = ?", (promo_id,))
    return cur.fetchall()


@transaction
def remove_all_kicked(channel_id):
    uids = []
    cur.execute(
        "UPDATE promos SET status = -1 WHERE status = 1 AND channel_id = ? RETURNING promo_id", (channel_id,)
    )

    if not (pids := cur.fetchall()):
        return uids
    pids = tuple(x[0] for x in pids)
    cur.execute(
        f"DELETE FROM subs WHERE promo_id IN ({', '.join(['?'] * len(pids))}) RETURNING user_id",
        pids
    )
    if res := cur.fetchall():
        uids += [x[0] for x in res]
    
    cur.execute(
        f"DELETE FROM reflinks WHERE promo_id IN ({', '.join(['?'] * len(pids))}) RETURNING user_id, reflink_id", #TODO return links to invoke after bot is kicked from channel
        pids
    )
    if res := cur.fetchall():
        uids += [x[0] for x in res]
        cur.execute(
            f"DELETE FROM joins WHERE reflink_id IN ({', '.join(['?'] * len(res))})",
            tuple(x[1] for x in res)
        )
    return uids
