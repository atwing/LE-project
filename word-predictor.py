from collections import defaultdict
import nltk
import pdb
import argparse
import codecs

MAX_PREDICTIONS = 10 # 10 # amount of words to predict given a sample

def build_conditional_probabilities(corpus):
    """
    The function takes as its input a corpus string (words separated by 
    spaces) and returns a 2D dictionary of probabilities P(next|current) of
    seeing a word "next" conditionnaly to seeing a word "current". 
    """

    # First we parse the string to build a double dimension dictionary that
    # returns the conditional probabilities.

    # We parse the string to build a first dictionary indicating for each
    # word, what are the words that follow it in the string. Repeated next
    # words are kept so we use a list and not a set. 

    tokenized_string = corpus.split()
    previous_word = ""
    dictionary = defaultdict(list)

    for current_word in tokenized_string:
        if previous_word != "":
            dictionary[previous_word].append(current_word)
        previous_word = current_word
        
    # We know parse dictionary to compute the probability each observed
    # next word for each word in the dictionary. 

    for key in dictionary.keys():
        next_words = dictionary[key]
        unique_words = set(next_words) # removes duplicated
        nb_words = len(next_words)
        probabilities_given_key = {}
        for unique_word in unique_words:
            probabilities_given_key[unique_word] = \
                float(next_words.count(unique_word)) / nb_words
        dictionary[key] = probabilities_given_key

    return dictionary


def bigram_next_word_predictor(conditional_probabilities, current, next_candidate):
    """
    The function takes as its input a 2D dictionary of probabilities 
    P(next|current) of seeing a word "next" conditionnaly to seeing a word 
    "current", the current word being read, and a next candidate word, and
    returns P(next_candidate|current).
    """

    # We look for the probability corresponding to the 
    # current -> next_candidate pair

    if conditional_probabilities.has_key(current):
        if conditional_probabilities[current].has_key(next_candidate):
            return conditional_probabilities[current][next_candidate]

    # If current -> next_candidate pair has not been observed in the corpus,
    # the corresponding dictionary keys will not be defined. We return 
    # a probability 0.0

    return 0.0

def process_input_file(input_filename):
    """
    Reads and processes the input file one word at a time.

    input_filename: The name of the input corpus file.
    return: extracted tokens from the corpus, None otherwise.
    """
    try:
        with codecs.open(input_filename, 'r', 'utf-8') as f:
            tokens = nltk.word_tokenize(f.read().lower())
        return tokens
    except IOError:
        print('Error reading input text file')
        return None

def main():
    # Read in corpus and predict next word based on n-gram probabilities

    # parser for input arguments
    parser = argparse.ArgumentParser(description='WordPredictor')
    parser.add_argument('--corpus', '-train', type=str, required=True, help='training corpus')
    parser.add_argument('--test', '-test', type=str, required=True, help='test sample')

    arguments = parser.parse_args()

    # read in training & test corpus and get tokens
    corpus = process_input_file(arguments.corpus)
    # corpus = "the cat is red the cat is green the cat is blue the dog is brown"
    sample = process_input_file(arguments.test)

    # get bigrams and their frequencies
    bigrams = nltk.ngrams(corpus, 2)
    bi_freq = nltk.ConditionalFreqDist(bigrams)
    # freqprob2 = nltk.ConditionalProbDist(freq2, nltk.MLEProbDist)

    # get trigrams and their frequencies
    trigrams = nltk.ngrams(corpus, 3)
    condition_pairs = (((w0, w1), w2) for w0, w1, w2 in trigrams)
    tri_freq = nltk.ConditionalFreqDist(condition_pairs)

    # print test sample before predicting words
    print('[Test sample]')
    print(' '.join(map(str, sample)))

    # predict next word of a sample phrase
    for i in range(MAX_PREDICTIONS):
        if tuple(sample[-2:]) not in tri_freq:
            if sample[-1] not in bi_freq:
                print('Word not found in bigram list.')
            else:
                sample.append(bi_freq[sample[-1]].max())
        else:
            sample.append(tri_freq[tuple(sample[-2:])].max())

    # output predicted words appended to test sample
    print('[Predicted phrase]')
    print(' '.join(map(str, sample)))

    # pdb.set_trace()
    
    # Some sample queries to the bigram predictor
    # assert bigram_next_word_predictor(conditional_probabilities, "the", "cat") == 0.75
    # assert bigram_next_word_predictor(conditional_probabilities, "is", "red") == 0.25
    # assert bigram_next_word_predictor(conditional_probabilities, "", "red") == 0.0

if __name__ == "__main__":
    main()