# Word Predictor (n-grams)
Language Engineering Project: 

## How to run the program:
- enter the test sentence in "test.txt"  
- run "word-predictor.py"
- if the test sentence exists in the corpus, the next word is returned
- if not, the user is asked to enter the next word
- the unknown words are subsequently added to the dictionary
- the number of predicted words can be adjusted in the program by altering the global variable MAX_PREDICTIONS 

## Usage example:
`$ python word-predictor.py --corpus kafka.txt --test test.txt --load`

###### Arguments:
--corpus: file containing training corpus  
--test: file with a test sample  
--load: load previously trained predictor model 