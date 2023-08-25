import argparse
import re
import sys
from typing import List, Union

import dotenv
from read_to_trie import read_files
from search.data_utils import AutoCompleteData
from search.search_completions import get_best_k_completion
from trie import Trie

PATTERN = r'[^a-zA-Z0-9\s]'


def input_validation(string: str) -> Union[str, None]:
    """
    Validate the user input.
    :param string: the user input.
    :return: the user input after validation.
    """
    clean_line = re.sub(PATTERN, '', string).lower().strip()
    if clean_line == '' or clean_line == '\n' or clean_line == ' ':
        print("You didn't enter a text.")
        return None
    else:
        print("You entered: " + clean_line)
        return clean_line


def user_input():
    """
    Get the user input.
    :return: the user input.
    """
    string = input("Enter your text:")
    return string


def init_db ( path_to_data: str ) -> (Trie, List[str]):
    """
    Initialize the database with the data from the files and return the trie and the data list
    :return: trie tree of the words, data list of the files.
    """
    trie_tree = Trie()
    data_list = []
    read_files(trie_tree, path_to_data, data_list, 0)
    return trie_tree, data_list


def init ( path_to_data: str ):
    """
    Initialize the search engine and return the trie and the data list.
    :return: trie tree of the words, data list of the files.
    """
    print("Welcome to the search engine!")
    print("Loading the database...")
    trie_tree, data_list = init_db(path_to_data)
    print("The search engine is ready to use!")
    return trie_tree, data_list


def main():
    parser = argparse.ArgumentParser(description="CLI interface for the project.")
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = dotenv.get_key(dotenv.find_dotenv(), "PATH_TO_DATA")
    trie_tree, data_list = init(path)
    print("This is a search engine for auto complete sentences.")
    print("Enter your text and get the best 5 auto complete sentences.")
    print("don't worry about spelling mistakes or lower/upper case, we will take care of it.")
    print("Enter 'exit' to exit the program.")
    while True:
        string = user_input()
        string = input_validation(string)
        if string is None:
            continue
        if string == "exit":
            break
        else:
            res: List[AutoCompleteData] = get_best_k_completion(string, trie_tree, data_list, 5)
            for index in range(len(res)):
                print(
                    f"{index + 1}. {' '.join(res[index].completed_sentence)}. ({res[index].source_text},"
                    f" {res[index].offset})")


if __name__ == "__main__":
    main()
