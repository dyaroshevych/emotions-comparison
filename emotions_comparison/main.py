"""Main module for running the films vs books analysis programme.

    Functions
    ---------
        print_conclusion - print the conclusion about the analysis
        input_until_valid - wait for the user to choose among some values
        get_particular_comparison - get comparison of one book vs one film
        get_analysis - get books vs films emotions and rating analysis
        main - run the programme
"""


from typing import List
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from emotions_comparison import emotions


START_MESSAGE = """
Do you want to compare emotions between a particular book and film (1)
or get an analysis based on H.G. Wells\' books (2)?
"""

BAR_WIDTH = 0.35

BOOKS_PATH = Path(__file__).parent / 'data/books.csv'
FILMS_PATH = Path(__file__).parent / 'data/films.csv'


def print_conclusion() -> None:
    """
    Print analysis conclusion.
    """
    print()
    print("""
As we can see, each emotion in the film has a better rate than a corresponding emotion in the book.
However, book still has better rating stats. The reason for such a phenomen is because films usually
try to make the viewer engaged by causing eccessive emotins, while books focus more on plot quality.
""")


def input_until_valid(valid_vals: List[int], message: str = '') -> int:
    """
    Let the user choose an integer value among the given valid ones.
    Ask user again until the input is valid.

    :param valid_vals: a list of acceptable values
    :param message: a message to print before user prompt
    :return: user's choice
    """
    if message:
        print(message)

    val = None

    while val not in valid_vals:
        try:
            val = int(input())

            if val not in valid_vals:
                raise ValueError
        except ValueError:
            print('Please, make a valid choice.')

    return val


def get_particular_comparison() -> None:
    """
    Let the user choose a book and a film for that book.
    Print comparison between that book and film.
    """
    # choose a book title
    df_books = pd.read_csv(BOOKS_PATH)
    titles = list(df_books['title'])

    print('Choose a book from the catalogue:')

    for idx, title in enumerate(titles):
        print(f'{title} ({idx + 1})')

    valid_choices = {i + 1 for i in range(df_books.shape[0])}

    chosen_idx = input_until_valid(valid_choices) - 1
    chosen_title = df_books['title'][chosen_idx]

    # choose film year
    df_films = pd.read_csv(FILMS_PATH)

    df_films = df_films.loc[df_films['title'] == chosen_title]

    years = list(df_films['year'])
    chosen_year = years[0]

    if len(years) > 1:
        print('Choose film creation year:')

        for idx, year in enumerate(years):
            print(f'{chosen_title} - {year} ({idx + 1})')

        valid_choices = {i for i, _ in enumerate(years, 1)}
        chosen_year = years[input_until_valid(valid_choices) - 1]

    # get emotion rates for book and film
    book_emotions = emotions.get_book_emotions(chosen_title)
    film_emotions = emotions.get_film_emotions(chosen_title, chosen_year)

    # print emotion rates
    emotions.print_emotions(chosen_title, f'{chosen_title} ({chosen_year})',
                            book_emotions, film_emotions)

    # print ratings
    book_info = df_books.loc[df_books['title']
                             == chosen_title].iloc[0, 1:3]
    film_info = df_films.loc[df_films['year']
                             == chosen_year].iloc[0, 2:4]

    print()
    print(f'Book rating: {book_info[0]} ({book_info[1]} votes)')
    print(f'Film rating: {film_info[0]} ({film_info[1]} votes)')

    print_conclusion()


def get_analysis() -> None:
    """
    Build a bar plot of films and books ratings.
    """
    df_books = pd.read_csv(BOOKS_PATH)
    df_films = pd.read_csv(FILMS_PATH)

    labels = [f'{row[1][0]} ({row[1][1]})' for row in df_films.iterrows()]

    books_means = [df_books.loc[df_books['title'] == title].iloc[0, 1]
                   for title in df_films['title']]
    films_means = list(df_films['average_rating'])

    x_loc = np.arange(len(labels))   # labels locations

    _, axes = plt.subplots()
    axes.bar(x_loc - BAR_WIDTH / 2, books_means, BAR_WIDTH,  label='Book')
    axes.bar(x_loc + BAR_WIDTH / 2, films_means, BAR_WIDTH,  label='Film')
    plt.xticks(x_loc, ha='right', rotation=45)

    # customize axes and labels
    axes.set_ylabel('Rating')
    axes.set_yticks(range(10))
    axes.set_title('Books vs Films Ratings')
    axes.set_xticks(x_loc)
    axes.set_xticklabels(labels)
    axes.legend()

    plt.subplots_adjust(left=0.15, bottom=0.4)

    print_conclusion()
    plt.show()


def main() -> None:
    """
    Show book and film analysis to the user.
    """
    mode = input_until_valid(set([1, 2]), START_MESSAGE)

    if mode == 1:
        get_particular_comparison()
    else:
        get_analysis()
