import time
import pywaves
import utils as utils
import logging, verboselogs, coloredlogs

from json.decoder import JSONDecodeError
from finder.update_top_wallets import get_top_wallets


def init_logger(level: str, name: str) -> logging.Logger:
    """ Init application logger """
    handler = logging.StreamHandler()

    handler.setFormatter(logging.Formatter("%(asctime)s (%(name)s): %(message)s"))

    log = verboselogs.VerboseLogger(name, level)
    log.addHandler(handler)

    coloredlogs.install(level=level, logger=log)

    return log


log = init_logger(logging.DEBUG, 'sf')

if __name__ == "__main__":
    top_wallets = get_top_wallets()
    checked_count = 0

    while True:
        seed = utils.seed(utils.random_words())
        try:
            address = pywaves.Address(seed=seed)
            # log.info("\tWallet ({}): {}".format(address.address, seed))
            if address.address in top_wallets:
                log.success("\tFound top wallet ({}): {}".format(address.address, seed))

            checked_count += 1
            if checked_count % 10000 == 0:
                log.info("Iterated: {}".format(checked_count))

        except ConnectionError as e:
            log.exception("Connection error", e)
            time.sleep(180)
            continue
        except JSONDecodeError as e:
            log.exception("JSONDecodeError error", e)
            time.sleep(180)
            continue

