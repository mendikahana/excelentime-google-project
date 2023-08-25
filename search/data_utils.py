from dataclasses import dataclass
from collections import namedtuple


SentenceIndex = namedtuple('SentenceIndex', ['file_id', 'sentence_id', 'position'])


@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int

    def __init__(self, sentence_index: SentenceIndex, sentence:str , score):
        self.completed_sentence = sentence
        self.source_text = get_file_name(sentence_index.file_id)
        self.offset = sentence_index.sentence_id
        self.score = score


def get_file_name(file_id: int) -> str:
    """
    function to get the file name by the file id.
    :param file_id: the file id.
    :return: the file name.
    """
    return f"input\\{file_id}.txt"