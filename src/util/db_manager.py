import sqlite3
import logging

conn = None

def init_db(path='../../db/local.db'):
    global conn
    try:
        conn = sqlite3.connect(path)
        
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS summoners (
            summonerId TEXT PRIMARY KEY,
            puuid TEXT
        );''')
        c.execute('''CREATE INDEX IF NOT EXISTS idx_summonerId ON summoners(summonerId);''')

        c.execute('''CREATE TABLE IF NOT EXISTS matches (
            matchId TEXT PRIMARY KEY
        );''')
        c.execute('''CREATE INDEX IF NOT EXISTS idx_matchId ON matches(matchId);''')
        conn.commit()
        logging.info('DB initialized')
        return conn
    except Exception as e:
        logging.error(f'Error initializing db: {e}')
        if conn:
            conn.close()
        conn = None
        return None

def close_db():
    if conn:
        conn.close()
        logging.info('DB closed')


def get_summoner(summonerId):
    c = conn.cursor()
    c.execute("SELECT puuid FROM summoners WHERE summonerId = ?", (summonerId,))
    result = c.fetchone()
    return result[0] if result else None

def insert_summoner(summonerId, puuid):
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO summoners (summonerId, puuid) VALUES (?, ?)", (summonerId, puuid))
    conn.commit()

def check_match_id(matchId):
    c = conn.cursor()
    c.execute("SELECT 1 FROM matches WHERE matchId = ?", (matchId,))
    result = c.fetchone()
    return result is not None

def update_match_id(matchId):
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO matches (matchId) VALUES (?)", (matchId,))
    conn.commit()