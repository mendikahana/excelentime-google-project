from unittest.mock import Mock, patch

import pytest
from search.data_utils import AutoCompleteData, SentenceIndex
from search.search_completions import *


def test_compare_indexes():
    list_of_indexes = [SentenceIndex(1, 1, 0), SentenceIndex(1, 1, 2), SentenceIndex(1, 5, 3)]
    list_of_indexes2 = [SentenceIndex(4, 1, 1), SentenceIndex(1, 1, 2), SentenceIndex(1, 1, 3)]
    res = compare_indexes(list_of_indexes, list_of_indexes2)
    assert len(res) == 1
    assert res[0] == SentenceIndex(1, 1, 2)


def test_filter_by_indexes():
    list_of_indexes = [SentenceIndex(1, 1, 0), SentenceIndex(1, 1, 2), SentenceIndex(1, 5, 3)]
    list_of_indexes2 = [SentenceIndex(4, 1, 1), SentenceIndex(1, 1, 2), SentenceIndex(1, 1, 3)]
    res = filter_by_indexes([list_of_indexes, list_of_indexes2])
    assert len(res) == 1
    assert res[0] == SentenceIndex(1, 1, 2)


def test_search_word():
    trie_tree_mock = Mock()
    trie_tree_mock.search.return_value = [SentenceIndex(1, 1, 0), SentenceIndex(1, 1, 2), SentenceIndex(1, 5, 3)]
    res = search_word('hello', trie_tree_mock)
    assert len(res) == 3
    assert res[0] == SentenceIndex(1, 1, 0)
    assert res[1] == SentenceIndex(1, 1, 2)
    assert res[2] == SentenceIndex(1, 5, 3)


def test_search_words():
    trie_tree_mock = Mock()
    trie_tree_mock.search.return_value = [SentenceIndex(1, 1, 1), SentenceIndex(1, 1, 2), SentenceIndex(1, 5, 3)]
    res = search_words(['hello', 'world'], trie_tree_mock)
    print(res)
    assert len(res) == 1
    assert res[0] == SentenceIndex(1, 1, 1)


def test_search():
    trie_tree_mock = Mock()
    trie_tree_mock.search.return_value = [SentenceIndex(1, 1, 1), SentenceIndex(1, 1, 2), SentenceIndex(1, 5, 3)]
    res = search('hello world', trie_tree_mock)
    assert len(res) == 1
    assert res[0] == SentenceIndex(1, 1, 1)
