import nltk
#The 'punkt' shpuld be downloaded once, afterwards hust apply the hash
#nltk.download('punkt')
from nltk.stem.porter import PorterStemmer
import numpy as np
stemmer = PorterStemmer()

def tokenize(sentence):
    return nltk.word_tokenize(sentence)


def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, words):
    # stem each word
    sentence_words = [stem(word) for word in tokenized_sentence]
    # initialize bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words: 
            bag[idx] = 1

    return bag

# Check that the tokenizing works well: ###########################################
"""
a = "How Are You?"
print(a)
a = tokenize(a)
print(a)
"""

# Check that the stemming works: ###########################################
"""
words = ['Universe', 'university', 'universal']
stemmed_words = [stem(w) for w in words]
print(stemmed_words)
"""

# Check that the bag_of_words works: ###########################################
"""
sentence = ["hello", "how", "are","you"]
words = ["hi", "hello", "I", "you","bye", "thank", "cool"]
bag = bag_of_words(sentence, words)
print(bag)
"""