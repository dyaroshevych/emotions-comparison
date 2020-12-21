"""Functions for calculating emotion rates of scripts.

    Functions
    ---------
        print_emotions - print a table of emotions in a book vs a film
        get_emotion_stats - transform a dataset of emotions
        get_word_counts - count each word in the file
        calculate_emotion_rates - calculate emotion rates of a dictionary
        get_script_emotions - calculate emotion rates of a file
        get_film_emotions - calculate emotion rates of a film script
        get_book_emotions - calculate emotion rates of a book
"""


from typing import Dict, List, Tuple
from pathlib import Path
from collections import Counter
from os import path
import pandas as pd


EMOTIONS = ['disgust', 'surprise', 'neutral',
            'anger', 'sad', 'happy', 'fear']
EMOTIONS_PATH = Path(__file__).parent / 'data/emotions.csv'


def print_emotions(book: str, film: str, book_emotions: List[str],
                   film_emotions: List[str]) -> None:
    """
    Print a table of emotions in a book vs a film.

    :param book: book title
    :param film: film title
    :param book_emotions: emotion rates for the book
    :param film_emotions: emotion rates for the film

    >>> print_emotions('book1', 'film1 (2020)',\
        [0.5, 0.2, 0.3, 0.4, 0.6, 0.7, 0.1], [1, 0.5, 0.7, 0.7, 1.3, 1.5, 0.2])
    <BLANKLINE>
    book1 [book] vs film1 (2020) [film]
          disgust  surprise  neutral  anger  sad  happy  fear
    BOOK      0.5       0.2      0.3    0.4  0.6    0.7   0.1
    FILM      1.0       0.5      0.7    0.7  1.3    1.5   0.2
    """
    results = pd.DataFrame(columns=EMOTIONS)

    book_row = {}
    film_row = {}

    for idx, emotion in enumerate(EMOTIONS):
        book_row[emotion] = book_emotions[idx]
        film_row[emotion] = film_emotions[idx]

    results = results.append(pd.Series(book_row, name='BOOK'))
    results = results.append(pd.Series(film_row, name='FILM'))

    print()
    print(f'{book} [book] vs {film} [film]')
    print(results)


def get_emotion_stats() -> Tuple[float]:
    """
    Transform a dataset of emotions to a dictionary of key-value pairs
    where keys are words and values are tuples of emotion rates.

    :return: a dictionary of emotion rates for each word

    >>> len(get_emotion_stats())
    1104
    >>> get_emotion_stats()['sky'][1]
    0.04407295
    >>> get_emotion_stats()['warning'][0]
    0.005494506
    """
    emotions_df = pd.read_csv(EMOTIONS_PATH)

    emotions = {}

    for row in emotions_df.iterrows():
        word = row[1][0][:-1]
        emotions[word] = tuple(row[1][1:])

    return emotions


def get_word_counts(filepath: str) -> Dict[str, int]:
    """
    Return a dictionary of key-value pairs where keys are words
    from the given file and values are their counts. If there is
    no such file, return an empty dictionary.

    :param filepath: path to the file
    :return: a dictionary of word counts

    >>> get_word_counts(Path('scripts/The Invisible Man 1933.txt'))['snow']
    6
    >>> get_word_counts(Path('scripts/The Time Machine 2002.txt'))['high']
    10
    """
    filepath = Path(__file__).parent / filepath

    if not path.exists(filepath):
        return None

    with open(filepath, 'r') as file:
        words = list(map(lambda word: word.strip('.,!?;:-').lower(),
                         file.readline().split(' ')))
        word_counts = dict(Counter(words))

    return word_counts


def calculate_emotion_rates(word_counts: Dict[str, int],
                            emotions: Dict[str, Tuple[float]]) -> List[float]:
    """
    Calculate emotion rate for a given dictionary of words.

    :param word_counts: a dictionary of words
    :param emotions: a dictionary of emotion rates for each word
    :return: a list of emotion rates
    """
    emotions_rate = [0] * len(EMOTIONS)
    total = 0

    for word, count in word_counts.items():
        if word not in emotions:
            continue

        total += count

        for idx, _ in enumerate(EMOTIONS):
            emotions_rate[idx] += emotions[word][idx]

    for idx, _ in enumerate(emotions_rate):
        emotions_rate[idx] *= 100 / total

    return emotions_rate


def get_script_emotions(filepath: str) -> List[float]:
    """
    Calculate overall emotion rates of a given file filled with words.

    :param filepath: path to a file filled with words
    :return: a list of emotion rate

    >>> get_script_emotions('scripts/The Invisible Man 2017.txt')[0]
    0.25946562144900015
    >>> get_script_emotions('scripts/The Invisible Man 2017.txt')[1]
    0.9596738795350731
    >>> len(get_script_emotions('scripts/The Invisible Man 2017.txt'))
    7
    """
    word_counts = get_word_counts(filepath)
    emotions = get_emotion_stats()

    return calculate_emotion_rates(word_counts, emotions)


def get_film_emotions(title: str, year: int) -> List[float]:
    """
    Calculate overall emotion rates of a given film script.

    :param title: film title
    :param year: film creation year
    :return: a list of emotion rates

    >>> get_film_emotions('The Invisible Man', 2017)[0]
    0.25946562144900015
    >>> get_film_emotions('The Invisible Man', 2017)[1]
    0.9596738795350731
    >>> len(get_film_emotions('The Invisible Man', 2017))
    7
    """
    scriptpath = f'scripts/{title} {year}.txt'

    return get_script_emotions(scriptpath)


def get_book_emotions(title: str) -> List[float]:
    """
    Calculate overall emotion rate of a given book.

    :param title: book title
    :return: a list of emotion rates

    >>> get_book_emotions('The Invisible Man')[0]
    0.14616658233345609
    >>> get_book_emotions('The Invisible Man')[1]
    0.42418248937038233
    >>> len(get_book_emotions('The Invisible Man'))
    7
    """
    bookpath = f'books/{title}.txt'

    return get_script_emotions(bookpath)
