# Google-Google-3

## System for Sentence Completion and Correction

### Data Structures:

1. **TrieNode**: Each node in the Trie represents a character in a word. It contains the following attributes:
   - `children`: An array of child nodes, indexed by character.
   - `wordLocation`: A list of `namedtuple('SentenceIndex', ['file_id', 'sentence_id', 'position'])` if the node represents the end of a sentence.
   - `isEndOfSentence`: Indicates if the node represents the end of a sentence.

2. **Trie**: The main Trie data structure contains a root node. It includes methods for insertion, search, sentence completion, and correction.

### Algorithms:

- **Insertion**: The `insert` method adds words to the Trie. It traverses the Trie character by character, creating new nodes as needed, and marking the end of words while updating the `wordLocation`.

- **Search**: The `search` method finds the location of a word in the Trie. It traverses the Trie character by character, returning a list of sentence locations where the word is found.

- **Sentence Completion**: By traversing the tree and finding the sentence index list, this algorithm identifies the intersection between all sentence indexes in order and returns the first 5 sentences.

- **Sentence Correction**: It examines each word and attempts to correct it based on scoring. The algorithm iterates through the words, eliminating sentences found until 5 valid sentences are obtained.

### Code Flow

#### Loading the Database:
1. Iterate through all the files in the directory.
2. Remove characters that are not letters or numbers.
3. Create a three-dimensional array to save the words in their original location.
4. Insert each word into the Trie database while saving the array location (SentenceIndex) at the end of the word.

#### Read Sentence from the User:
1. Remove characters that are not letters or numbers.
2. Iterate over each word in the Trie tree while retrieving all the positions of each word in the array.
3. Find the intersection between all words in order and return the first 5 sentences.

#### If the Number of Sentences is Less Than 5:
1. Iterate through all letters in each word in the scoring order and send them to the Trie to fix.
2. Find the intersection between all words in order and return the first missing sentence.

This system offers functionality for sentence completion and correction, making it valuable for applications such as auto-completion, spell checking, and natural language processing.
"# excelentime-google-project" 
