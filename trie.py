from collections import namedtuple
from typing import List, Union

NUM_OF_CHARS = 36

SentenceIndex = namedtuple('SentenceIndex', ['file_id', 'sentence_id', 'position'])


class TrieNode:
    """
    TrieNode represents a node in the Trie data structure.
    """

    def __init__(self):
        self.children: List[Union[TrieNode, None]] = [None] * NUM_OF_CHARS
        self.word_location: List[SentenceIndex] = []
        self.isEndOfWord = False


class Trie:
    """
    Trie is a data structure for efficient word insertion and searching.
    """

    def __init__(self):
        self.root = self.get_node()

    @staticmethod
    def get_node() -> TrieNode:
        """
        Returns a new TrieNode (initialized to NULLs).
        """
        return TrieNode()

    @staticmethod
    def char_to_index(ch) -> int:
        """
        Converts the given character into an index (0-25) assuming lowercase 'a' to 'z',
        and 0-9 to character into index (26-35).
        """
        if ch.isalpha():
            return ord(ch.lower()) - ord('a')
        return ord(ch) - ord('0') + 26

    @staticmethod
    def index_to_char(index: int) -> chr:
        """
        Converts the given index into a char (0-25) assuming lowercase 'a' to 'z',
        and 0-9 to character into index (26-35).
        """
        if index < 26:
            return chr((ord('a') + index))
        else:
            return chr((ord('0') + index - 26))

    def insert(self, key: str, file_id: int, row_number: int, word_index: int) -> None:
        """
        Inserts a word into the Trie.

        Args:
            key (str): The word to be inserted.
            file_id (int): The file id.
            row_number (int): The word number of the row.
            word_index (int): The word index in the sentence.

        Returns:
            None
        """
        p_crawl = self.root
        for level in key:
            index = self.char_to_index(level)
            if not p_crawl.children[index]:
                p_crawl.children[index] = self.get_node()
            p_crawl = p_crawl.children[index]

        # Mark the last node as the end of the word
        p_crawl.word_location.append(SentenceIndex(file_id, row_number, word_index))
        p_crawl.isEndOfWord = True

    def search(self, key: str) -> List[SentenceIndex]:
        """
        Searches for a word in the Trie.

        Args:
            key (str): The word to be searched.

        Returns:
            List[SentenceIndex]: A list of SentenceIndex named-tuples representing
            the locations where the word is found.
        """
        p_crawl = self.root
        for level in key:
            index = self.char_to_index(level)
            if not p_crawl.children[index]:
                return []
            p_crawl = p_crawl.children[index]
        return p_crawl.word_location

    def search_from(self, node: TrieNode, word: str) -> Union[TrieNode, None]:
        """
        Traverses the Trie from a given node to find the TrieNode corresponding to the end of the given word.

        Args:
            node (TrieNode): The starting node to begin the traversal.
            word (str): The word for which to find the corresponding node.

        Returns:
            TrieNode: The TrieNode corresponding to the end of the given word, or None if not found.
        """
        for level in word:
            index = self.char_to_index(level)
            if not node.children[index]:
                return None
            node = node.children[index]
        return node

    def add_letter(self, key: str, index: int) -> List[str]:
        """
        Adds a letter at a specific index in the given word and returns a list of valid words.

        Args:
            key (str): The word to which to add a letter.
            index (int): The index at which to add the letter.

        Returns:
            List[str]: A list of valid words formed by adding a letter at the specified index.
        """
        if index >= len(key):
            return []
        words = []
        p_crawl = self.search_from(self.root, key[:index])
        for letter_index in range(NUM_OF_CHARS):
            if p_crawl and p_crawl.children[letter_index]:
                p_crawl_temp = p_crawl.children[letter_index]
                p_crawl_temp = self.search_from(p_crawl_temp, key[index:])
                if p_crawl_temp and p_crawl_temp.isEndOfWord:
                    words.append(key[:index] + self.index_to_char(letter_index) + key[index:])
        return words

    def change_letter(self, key: str, index: int) -> List[str]:
        """
        Changes a letter at a specific index in the given word and returns a list of valid words.

        Args:
            key (str): The word in which to change a letter.
            index (int): The index at which to change the letter.

        Returns:
            List[str]: A list of valid words formed by changing a letter at the specified index.
        """
        if index >= len(key):
            return []
        words = []
        p_crawl = self.search_from(self.root, key[:index])
        for letter_index in range(NUM_OF_CHARS):
            if letter_index == self.char_to_index(key[index]):
                continue
            if p_crawl and p_crawl.children[letter_index]:
                p_crawl_temp = p_crawl.children[letter_index]
                p_crawl_temp = self.search_from(p_crawl_temp, key[index + 1:])
                if p_crawl_temp and p_crawl_temp.isEndOfWord:
                    words.append(key[:index] + self.index_to_char(letter_index) + key[index + 1:])
        return words

    def remove_letter(self, key: str, index: int) -> List[str]:
        """
        Removes a letter at a specific index in the given word and returns a list of valid words.

        Args:
            key (str): The word from which to remove a letter.
            index (int): The index at which to remove the letter.

        Returns:
            List[str]: A list of valid words formed by removing a letter at the specified index.
        """
        if index >= len(key):
            return []
        if self.search(key[:index] + key[index + 1:]):
            return [key[:index] + key[index + 1:]]
        return []
