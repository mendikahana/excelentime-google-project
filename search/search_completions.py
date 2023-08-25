from typing import List, Tuple

from search.data_utils import AutoCompleteData, SentenceIndex
from search.logic import find_sentence_by_indexes
from trie import Trie
from collections import defaultdict


def get_best_k_completion ( prefix: str, trie_tree: Trie, data_list: List[str], k: int = 5 ) -> List[AutoCompleteData]:
    """
    function to get the best k completions from the database.
    :param trie_tree:
    :param prefix: string of words that user input
    :param data_list: list of the sentences.
    :param k: number of the best completions to return.
    :return: a list of AutoCompleteData objects
    """
    sentences_indexes = search(prefix, trie_tree)
    if len(sentences_indexes) < k:  # find error correction
        find_error_correction(prefix, sentences_indexes, trie_tree, k - len(sentences_indexes))
    sentences_indexes = sentences_indexes[:k]
    lst_of_auto_complete_data = [
        AutoCompleteData(sentence_index, find_sentence_by_indexes(sentence_index, data_list), len(prefix)) for
        sentence_index in sentences_indexes if sentence_index]
    return lst_of_auto_complete_data


def search(user_input: str, trie_tree, shift: int = 1) -> List[SentenceIndex]:
    """
    function to search_test the autocomplete sentences from the database.
    :param user_input: string of words that user input
    :param trie_tree: the trie tree of the database.
    :param shift: the shift between the words. (for finding the words in a sentence with a gap between them)
    :return: a list of sentences that match the user input.
    """
    words = user_input.split()
    indexes = search_words(words, trie_tree, shift)
    return indexes


def search_word(word: str, trie_tree) -> List[SentenceIndex]:
    """
    function to search_test the autocomplete sentences from the database.
    :param trie_tree:
    :param word: word to search_test in Trie tree.
    :return: a list of tuples of indexes of: (file_id, sentence_id, position)
    """
    return trie_tree.search(word)


def search_words(words: List[str], trie_tree, shift: int = 1) -> List[SentenceIndex]:
    """
    function to search_test the autocomplete sentences from the database.
    :param trie_tree:
    :param words: list of words to search_test in Trie tree.
    :param shift: the shift between the words. (for finding the words in a sentence with a gap between them)
    :return: a list of tuples of indexes of: (file_id, sentence_id, position)
    """
    indexes = [search_word(word, trie_tree) for word in words]
    return filter_by_indexes(indexes, shift)


def filter_by_indexes(indexes: List[List[SentenceIndex]], shift: int = 1) -> List[SentenceIndex]:
    """
    function to filter the autocomplete sentences by indexes.
    :param indexes: list of lists of indexes of: (file_id, sentence_id, position)
    :param shift: the shift between the words. (for finding the words in a sentence with a gap between them)
    :return: a list of tuples of indexes of: (file_id, sentence_id, position)
    """
    res = indexes[0]
    if len(indexes) == 1:
        return res
    for i in range(1, len(indexes)):
        res = compare_indexes(res, indexes[i], shift + i - 1)
    return res


def compare_indexes(indexes_of_first_word: List[SentenceIndex],
                    indexes_of_second_word: List[SentenceIndex], shift: int = 1) -> List[SentenceIndex]:
    """
    function to compare the indexes of two words.
    :param indexes_of_first_word: list of indexes of the first word.
    :param indexes_of_second_word: list of indexes of the second word.
    :param shift: the shift between the words. (for finding the words in a sentence with a gap between them)
    :return: a list of tuples of indexes of: (file_id, sentence_id, position)
    """
    # this is a refactor of the code to improve the run time.
    # by using a dictionary to group the indexes by the file_id and sentence_id. of the second word.
    grouped_indexes = defaultdict(list)
    for index in indexes_of_second_word:
        grouped_indexes[(index.file_id, index.sentence_id)].append(index.position)

    res = []
    # now i only need to iterate over the indexes of the first word.
    # (the first word is the one that has less indexes because it is usally already was comaperaed to all the other
    # words above it in the sentence)
    for index in indexes_of_first_word:
        if (index.file_id, index.sentence_id) in grouped_indexes:
            second_word_positions = grouped_indexes[(index.file_id, index.sentence_id)]
            for position in second_word_positions:
                second_word_position = position - shift
                if index.position == second_word_position:
                    res.append(index)
                elif index.position < second_word_position:
                    break

    return res


def find_closest_correction(word: str, score: int, trie_tree: Trie):
    # word_indexes = []
    optional_words = []
    if score == 1:
        if len(word) >= 5:
            for index in range(4, len(word)):
                optional = trie_tree.change_letter(word, index)
                if optional:
                    optional_words.append(optional)
    elif score == 2:
        if len(word) >= 5:
            for index in range(4, len(word)):
                optional = trie_tree.remove_letter(word, index)
                if optional:
                    optional_words.append(optional)
                optional = trie_tree.add_letter(word, index)
                if optional:
                    optional_words.append(optional)
        if len(word) >= 4:
            optional = trie_tree.change_letter(word, 3)
            if optional:
                optional_words.append(optional)
    elif score == 3:
        if len(word) >= 3:
            optional = trie_tree.change_letter(word, 2)
            if optional:
                optional_words.append(optional)
    elif score == 4:
        if len(word) >= 4:
            optional_words.append(trie_tree.remove_letter(word, 3))
            optional_words.append(trie_tree.add_letter(word, 3))
        if len(word) >= 2:
            optional_words.append(trie_tree.change_letter(word, 1))
    elif score == 5:
        optional_words.append(trie_tree.change_letter(word, 0))
    elif score == 6:
        if len(word) >= 3:
            optional_words.append(trie_tree.remove_letter(word, 2))
            optional_words.append(trie_tree.add_letter(word, 2))
    elif score == 8:
        if len(word) >= 2:
            optional_words.append(trie_tree.remove_letter(word, 1))
            optional_words.append(trie_tree.add_letter(word, 1))
    elif score == 10:
        optional_words.append(trie_tree.remove_letter(word, 0))
        optional_words.append(trie_tree.add_letter(word, 0))

    # for optional_word in optional_words:
    #    word_indexes.append(search(optional_word, trie_tree))
    # return word_indexes
    uniq_words = set()
    for optional_word in optional_words:
        uniq_words = uniq_words.union(set(optional_word))
    return uniq_words


def find_error_correction(prefix, sentences_indexes, trie_tree, k):
    split_prefix = prefix.split(" ")
    if len(split_prefix) == 1:
        for score in range(1, 11):
            optional_words = find_closest_correction(prefix, score, trie_tree)
            for optional_word in optional_words:
                sentences_indexes += (search(optional_word, trie_tree))
            if len(sentences_indexes) >= k:
                return
    else:
        correction_result = []
        for index in range(len(split_prefix)):
            optional_error_word = split_prefix[index]
            for score in range(1, 11):
                optional_words = find_closest_correction(optional_error_word, score, trie_tree)
                for optional_word in optional_words:
                    optional_sentence = split_prefix
                    optional_sentence[index] = optional_word
                    sentences_indexes += (search_words(optional_sentence, trie_tree))
                    if len(sentences_indexes) >= k:
                        return
