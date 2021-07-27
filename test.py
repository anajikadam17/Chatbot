import random
import json
import tensorflow as tf
import tflearn
# from tensorflow.python.framework import ops
from tensorflow.keras.models import load_model
# from keras.models import load_model 
import numpy as np
import pickle
import nltk
nltk.download('punkt')
nltk.download('wordnet')


from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

intents = json.loads(open(r'resources/data/intents.json').read())
# restoring all the data structures
data = pickle.load( open(r"resources/pickles/training_data_pkl", "rb" ) )
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

ERROR_THRESHOLD = 0.30

# load the saved model
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 10)
net = tflearn.fully_connected(net, 10)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)
model = tflearn.DNN(net)
model.load('resources/models/tflearn/model.tflearn')


def clean_up_sentence(sentence):
    # tokenizing the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stemming each word
    # sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# returning bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenizing the pattern
    sentence_words = clean_up_sentence(sentence)
    # generating bag of words
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

ERROR_THRESHOLD = 0.15
def classify(sentence):
    # generate probabilities from the model
    results = model.predict([bow(sentence, words)])[0]
    # filter out predictions below a threshold
    # print(results)
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    # print(results)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    # print(return_list)
    return return_list

CALL_BACK = 0.75
def response(sentence):
    results = classify(sentence)
    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        while results:
            for i in intents['intents']:
                # if score is less than CALL_BACK then return specific responce last intent
                if results[0][1] < CALL_BACK:
                    # a random response from the intent
                    return random.choice(intents['intents'][-1]['responses']), None
                # find a tag matching the first result
                if i['tag'] == results[0][0]:
                    tag = results[0][0]
                    # a random response from the intent
                    return random.choice(i['responses']), tag
            results.pop(0)


def main():
    
    def classify(sentence):
        # generate probabilities from the model
        results = model.predict([bow(sentence, words)])[0]
        # filter out predictions below a threshold
        results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append((classes[r[0]], r[1]))
        # return tuple of intent and probability
        return return_list

    def response(sentence, userID='123', show_details=False):
        results = classify(sentence)
        # if we have a classification then find the matching intent tag
        if results:
            # loop as long as there are matches to process
            while results:
                for i in intents['intents']:
                    # find a tag matching the first result
                    if i['tag'] == results[0][0]:
                        # a random response from the intent
                        return random.choice(i['responses'])
                results.pop(0)
    
    while True:
        inp = input('You:\t')
        if inp == 'exit':
            break
        else:
            chatbot_result = response(inp)
            print(f'bot:\t{chatbot_result}')
            
if __name__ == '__main__':
    print('TYPE "exit" TO QUIT!')
    main()
