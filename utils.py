import secrets
from pywaves.address import wordList


def random_words(length: int = 15) -> list:
    words = []
    for i in range(length):
        words.append(secrets.choice(wordList))

    return words


def seed(words: list) -> str:
    return ' '.join(words)
