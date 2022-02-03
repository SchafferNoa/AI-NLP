import nltk
from nltk.stem.porter import PorterStemmer
import numpy as np
stemmer = PorterStemmer()


def tokenize(sentence):
    return nltk.word_tokenize(sentence)


def stem(word):
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, words):
    # first, stem each word
    sentence_words = [stem(word) for word in tokenized_sentence]
    # then, initialize bag of words with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words:
            bag[idx] = 1

    return bag


################################# Validate the tokenizing #################################
"""
a = "Hello world!"
print(a)
a = tokenize(a)
print(a)
"""

################################# Validate the stemming #################################
"""
words = ['Star', 'staring', 'starry']
stemmed_words = [stem(w) for w in words]
print(stemmed_words)
"""

################################# Validate the bag_of_words #################################
"""
sentence = ["hello", "how", "are","you"]
words = ["hi", "hello", "I", "you","bye", "thank", "cool"]
bag = bag_of_words(sentence, words)
print(bag)
"""
