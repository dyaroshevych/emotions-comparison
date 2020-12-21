"""Functions for transofrmation of films and books datasets.

    Functions
    ---------
        get_books_ratings - transform books dataset
        get_films_ratings - transform films dataset
        generate_datasets - generate films and books datasets
"""


from typing import Set
import pandas as pd
from pathlib import Path
from os import mkdir, path


BOOKS_LOCATION = Path(__file__).parent / 'raw_data/books.csv'
FILMS_LOCATIONS = [Path(__file__).parent / 'raw_data/title.basics.tsv',
                   Path(__file__).parent / 'raw_data/title.ratings.tsv']

BOOKS_COLS = {'original_title': 'title', 'ratings_count': 'num_votes'}
FILMS_COLS = {'originalTitle': 'title', 'startYear': 'year',
              'averageRating': 'average_rating', 'numVotes': 'num_votes'}


def get_books_ratings(location: str) -> pd.DataFrame:
    """
    Read data from books rating dataset, select
    H.G. Wells' books and remove unnecessary data.

    :param location: location of the dataset
    :return: transformed data

    >>> get_books_ratings(BOOKS_LOCATION)
                          title  average_rating  num_votes
    0          The Time Machine            7.74     276076
    1     The War of the Worlds            7.60     159752
    2         The Invisible Man            7.24      84778
    3  The Island of Dr. Moreau            7.44      60346
    """
    dataframe = pd.read_csv(location, low_memory=False)

    dataframe = dataframe.loc[(dataframe['authors'].str.contains(
        'H.G. Wells')) & (~dataframe['language_code'].isnull())]

    # transform rating from 0-5 to 0-10 system
    dataframe['average_rating'] *= 2

    # only keep columns with title, rating and ratings count
    dataframe = dataframe.loc[:, ['original_title', 'average_rating',
                                  'ratings_count']].reset_index(drop=True)

    # rename columns
    dataframe.rename(columns=BOOKS_COLS, inplace=True)

    return dataframe


def get_films_ratings(location_1: str, location_2: str, books: Set[str]) -> pd.DataFrame:
    """
    Read and transform data from two film datasets, only
    selecting corresponding films for the given set of books.

    :param location_1: location of film titles dataset
    :param location_1: location of film ratings dataset
    :param books: a set of books to select films to
    :return: a dataframe with films ratings

    >>> get_films_ratings(*FILMS_LOCATIONS, {'The Time Machine', 'The Island of Dr. Moreau',\
                                            'The Invisible Man', 'The War of the Worlds'})
                          title  year  average_rating  num_votes
    0         The Invisible Man  1933             7.7      30172
    1     The War of the Worlds  1953             7.1      32429
    2          The Time Machine  1960             7.6      35786
    3  The Island of Dr. Moreau  1977             5.9       5677
    4  The Island of Dr. Moreau  1996             4.6      30894
    5          The Time Machine  2002             6.0     117796
    6         The Invisible Man  2020             7.1     152154
    7         The Invisible Man  2017             3.3        168
    """
    # read title basics data
    df_basics = pd.read_csv(location_1, sep='\t', low_memory=False)
    df_ratings = pd.read_csv(location_2, sep='\t', low_memory=False)

    # remove unfilled data
    df_basics = df_basics.loc[(df_basics['originalTitle'].isin(books))
                              & (df_basics['titleType'] == 'movie')
                              & (df_basics['startYear'] != '\\N')
                              & (df_basics['runtimeMinutes'] != '\\N')]

    # merge datasets and remove unused columns
    merged_df = pd.merge(
        df_basics[['tconst', 'originalTitle', 'startYear']], df_ratings, on=["tconst"])
    merged_df.drop(['tconst'], axis=1, inplace=True)

    # rename columns
    merged_df.rename(columns=FILMS_COLS, inplace=True)

    return merged_df


def generate_datasets() -> None:
    """
    Generate books and films datasets.
    """
    books_df = get_books_ratings(BOOKS_LOCATION)
    book_titles = set(books_df['title'])

    films_df = get_films_ratings(*FILMS_LOCATIONS, book_titles)

    if not path.exists('data'):
        mkdir('data')

    # save datasets
    books_df.to_csv(Path('data/books.csv'), index=False)
    films_df.to_csv(Path('data/films.csv'), index=False)
