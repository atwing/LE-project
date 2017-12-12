from collections import defaultdict
from nltk.collocations import *
import nltk
import pdb
import argparse
import codecs
import pickle

MAX_PREDICTIONS = 10 # 10 # amount of words to predict given a sample

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
    parser.add_argument('--load', action='store_true', help='load trained model')

    arguments = parser.parse_args()

    # read in training & test corpus and get tokens
    corpus = process_input_file(arguments.corpus)
    # corpus = "the cat is red the cat is green the cat is blue the dog is brown"
    sample = process_input_file(arguments.test)

    if arguments.load:
        # load from file if --load argument given
        with open("bi_freq.pkl", "rb") as f:
            bi_freq = pickle.load(f)
        with open("tri_freq.pkl", "rb") as f:
            tri_freq = pickle.load(f)
    else:
        # get bigrams and their frequencies
        bigrams = nltk.ngrams(corpus, 2)
        bi_freq = nltk.ConditionalFreqDist(bigrams)
        # freqprob2 = nltk.ConditionalProbDist(freq2, nltk.MLEProbDist)

        # get trigrams and their frequencies
        trigrams = nltk.ngrams(corpus, 3)
        condition_pairs = (((w0, w1), w2) for w0, w1, w2 in trigrams)
        tri_freq = nltk.ConditionalFreqDist(condition_pairs)

        # save probability lists
        with open("bi_freq.pkl", "wb") as f:
            pickle.dump(bi_freq, f, pickle.HIGHEST_PROTOCOL)
        with open("tri_freq.pkl", "wb") as f:
            pickle.dump(tri_freq, f, pickle.HIGHEST_PROTOCOL)

    # print test sample before predicting words
    print('[Test sample]')
    print(' '.join(map(str, sample)))

    # predict next word of a sample phrase
    for i in range(MAX_PREDICTIONS):
        if tuple(sample[-2:]) not in tri_freq:
            # check bigram probabilities if two words don't exist in trigram list            
            if sample[-1] not in bi_freq:
                print('Word not found in bigram list.')
                in_str = raw_input("Please input word after '" + str(sample[-1]) + "': ")
                bi_freq[sample[-1]][in_str] += 1
                tri_freq[tuple(sample[-2:])][in_str] += 1

                # save updated lists
                with open("bi_freq.pkl", "wb") as f:
                    pickle.dump(bi_freq, f, pickle.HIGHEST_PROTOCOL)
                with open("tri_freq.pkl", "wb") as f:
                    pickle.dump(tri_freq, f, pickle.HIGHEST_PROTOCOL)
            else:
                sample.append(bi_freq[sample[-1]].max())
        else:
            sample.append(tri_freq[tuple(sample[-2:])].max())

    # output predicted words appended to test sample
    print('[Predicted phrase]')
    print(' '.join(map(str, sample)))

    # fourgrams=nltk.collocations.QuadgramCollocationFinder.from_words(corpus)
    # for fourgram, freq in fourgrams.ngram_fd.items():  
    #     print fourgram, freq

    pdb.set_trace()
    
    # Some sample queries to the bigram predictor
    # assert bigram_next_word_predictor(conditional_probabilities, "the", "cat") == 0.75
    # assert bigram_next_word_predictor(conditional_probabilities, "is", "red") == 0.25
    # assert bigram_next_word_predictor(conditional_probabilities, "", "red") == 0.0

if __name__ == "__main__":
    main()