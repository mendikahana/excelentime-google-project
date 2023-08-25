from trie import Trie
from typing import List
import sys
import os
import re

pattern = r'[^a-zA-Z0-9\s]'


def store_file_data(trie: Trie, file_path: str, file_index: int):
    with open(file_path, 'r', encoding='utf-8') as file:
        line_list = []
        line_number = 0
        for line in file:
            clean_line = re.sub(pattern, '', line).lower().strip()
            words_list = []
            if clean_line == '' or clean_line == '\n' or clean_line == ' ':
                continue
            for word_number, word in enumerate(clean_line.split(), start=0):
                trie.insert(word, file_index, line_number, word_number)
                words_list.append(word)
            if len(words_list) > 0:
                line_list.append(words_list)
                line_number += 1
        return line_list


def read_files(trie: Trie, dir_path: str, arr: List, file_index: int = 0) -> int:
    """
    Recursively reads and processes text files in a directory, inserting words into a Trie.

    Args:
        trie (Trie): The Trie data structure to insert words into.
        dir_path (str): The path to the directory containing text files.
        arr(List): A three-dimensional array for saving the words in the original location
        file_index (int, optional): The current file index (used internally for recursion). Default is 0.

    Returns:
        int: The last file id

    """
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        if os.path.isfile(file_path):
            if file_name.endswith(".txt"):
                line_list = store_file_data(trie, file_path, file_index)
                if len(line_list) > 0:
                    file_index += 1
                    arr.append(line_list)
        else:
            file_index = read_files(trie, file_path, arr, file_index)
    return file_index


# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         trie_s = Trie()
#         data_list = []
#         read_files(trie_s, sys.argv[1], data_list,  0)
#         print(trie_s.search("python"))
#         print(data_list[808][2755][1])
#         print(trie_s.add_letter("pyhon", 2))
#         print(trie_s.change_letter("pyxhon", 2))
#         print(trie_s.change_letter("oython", 0))
#         print(trie_s.add_letter("ython", 0))
