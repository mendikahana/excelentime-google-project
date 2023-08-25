from search.data_utils import SentenceIndex
from typing import List


def find_sentence_by_indexes(indexes: SentenceIndex, data_list: List[str]) -> str:
    """
    function to find the sentences by the indexes.
    :param indexes: list of indexes of: (file_id, sentence_id, position)
    :param data_list: list of the sentences.
    :return: the complete sentence.
    """
    return data_list[indexes.file_id][indexes.sentence_id]





