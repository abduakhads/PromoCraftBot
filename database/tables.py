users = """CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    lang TEXT NOT NULL,
    fullname TEXT NOT NULL,
    username TEXT NOT NULL
)"""

promos = """CREATE TABLE IF NOT EXISTS promos (
    promo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    winner_count INTEGER NOT NULL,
    expiration TEXT NOT NULL,
    memberlimit TEXT NOT NULL,
    status INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
)"""

reflinks = """CREATE TABLE IF NOT EXISTS reflinks (
    reflink_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    promo_id INTEGER NOT NULL,
    link TEXT NOT NULL,
    revoked INTEGER NOT NULL,
    joins INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (promo_id) REFERENCES promos (promo_id)
)"""
