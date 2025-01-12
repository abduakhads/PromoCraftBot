users = """CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    lang TEXT NOT NULL,
    fullname TEXT NOT NULL,
    username TEXT NOT NULL,
    timediff TEXT
)"""

promos = """CREATE TABLE IF NOT EXISTS promos (
    promo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    mode TEXT NOT NULL,
    title TEXT NOT NULL,
    winner_count INTEGER NOT NULL,
    expiration TEXT NOT NULL,
    memberlimit INTEGER,
    status INTEGER DEFAULT 1,
    winners INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (channel_id) REFERENCES channels (channel_id)
)"""

reflinks = """CREATE TABLE IF NOT EXISTS reflinks (
    reflink_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    promo_id INTEGER NOT NULL,
    link TEXT NOT NULL,
    revoked INTEGER DEFAULT 0,
    joins INTEGER DEFAULT 0,
    is_sub INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (promo_id) REFERENCES promos (promo_id)
)"""

subs = """CREATE TABLE IF NOT EXISTS subs (
    sub_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    promo_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (promo_id) REFERENCES promos (promo_id)
)"""

channels = """CREATE TABLE IF NOT EXISTS channels (
    channel_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    link TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
)"""

joins = """CREATE TABLE IF NOT EXISTS joins (
    reflink_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    FOREIGN KEY (reflink_id) REFERENCES reflinks (reflink_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (channel_id) REFERENCES channels (channel_id)
)"""