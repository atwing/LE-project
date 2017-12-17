# Word Prediction (n-grams)
Language Engineering Project: 

## TODO:
- (done) replace w/ nltk
- (done) try other policy than maximum likelihood
	- predict next word
		- **if word does not exist in trigrams, use bigrams for known word**
- compare BIGRAM / TRIGRAM / (QUADGRAM)
	- (implement fourgrams)
- (done) implement learning from new data/test data
- (suggestions: get top 3 probabilities and randomly choose one)

## How to run the program:
- enter the test sentence in "test.txt"  
- run "word-predictor.py" (python word-predictor.py --corpus kafka.txt --test test.txt)
- if the test sentence exists in the corpus, the next word is returned
- if not, the user is asked to enter the next word
- the unknown words are subsequently added
- the number of predicted words can be adjusted in the program by altering the MAX_PREDICTIONS global variable
