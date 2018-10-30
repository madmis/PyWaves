import os
import datetime
import time
import pywaves
import sqlite3
import secrets
from pywaves.address import wordList
from requests.exceptions import ConnectionError
import logging, verboselogs, coloredlogs
from json.decoder import JSONDecodeError

conn = sqlite3.connect('/var/www/data/seeds.db')
c = conn.cursor()

t = ('seeds',)
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", t)
if not c.fetchone():
    c.execute('''CREATE TABLE seeds
                 (seed VARCHAR(150) NOT NULL,
                  wallet VARCHAR(50) NOT NULL,
                  bal VARCHAR(50) NOT NULL,
                  created DATETIME NOT NULL,
                  bal VARCHAR(20) NOT NULL
                  )''')
    c.execute('''CREATE UNIQUE INDEX seed_idx ON seeds (seed);''')
    conn.commit()


def init_logger(level: str, name: str) -> logging.Logger:
    """ Init application logger """
    handler = logging.StreamHandler()

    handler.setFormatter(logging.Formatter("%(asctime)s (%(name)s): %(message)s"))

    log = verboselogs.VerboseLogger(name, level)
    log.addHandler(handler)

    coloredlogs.install(level=level, logger=log)

    return log


log = init_logger(logging.DEBUG, 'bf')

while True:
    words = []
    for i in range(15):
        words.append(secrets.choice(wordList))

    seed = ' '.join(words)
    log.info(f"Seed: {seed}.")
    c.execute("SELECT seed FROM seeds WHERE seed=?", (seed,))
    if c.fetchone():
        log.warning("\t -- Seed checked before -- ")
        continue
    try:
        address = pywaves.Address(seed=seed)
        bal = address.balance()
        if bal > 0:
            log.success("\tBalance ({}): {}".format(address.address, address.balance()))
        else:
            log.info("\tBalance ({}): {}".format(address.address, address.balance()))
    except ConnectionError as e:
        log.exception("\tConnection error", e)
        time.sleep(180)
        continue
    except JSONDecodeError as e:
        log.exception("\tJSONDecodeError error", e)
        time.sleep(180)
        continue

    c.execute("INSERT INTO seeds VALUES (?,?,?,?)", (seed, address.address, datetime.datetime.now(),str(bal)))
    conn.commit()
    if bal > 0:
        break
