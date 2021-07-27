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

def main():
    words = []
    classes = []
    documents = []
    ignore = ['?']
    # loop through each sentence in the intent's patterns
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            # tokenize each and every word in the sentence
            w = nltk.word_tokenize(pattern)
            # add word to the words list
            
            # sentence_words = clean_up_sentence(pattern)
            words.extend(w)
            # add word(s) to documents
            documents.append((w, intent['tag']))
            # add tags to our classes list
            if intent['tag'] not in classes:
                classes.append(intent['tag'])
    # Perform stemming and lower each word as well as remove duplicates
    # words = [stemmer.stem(w.lower()) for w in words if w not in ignore]
    words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore]
    words = sorted(list(set(words)))
    # remove duplicate classes
    classes = sorted(list(set(classes)))

    # print (len(documents), "documents")
    # print (len(classes), "classes", classes)
    # print (len(words), "unique stemmed words", words)

    # create training data
    training = []
    output = []
    # create an empty array for output
    output_empty = [0] * len(classes)

    # create training set, bag of words for each sentence
    for doc in documents:
        # initialize bag of words
        bag = []
        # list of tokenized words for the pattern
        pattern_words = doc[0]
        # stemming each word
        # pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
        pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
        # create bag of words array
        for w in words:
            bag.append(1) if w in pattern_words else bag.append(0)

        # output is '1' for current tag and '0' for rest of other tags
        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1

        training.append([bag, output_row])

    # shuffling features and turning it into np.array
    random.shuffle(training)
    training = np.array(training)

    # creating training lists
    train_x = list(training[:,0])
    train_y = list(training[:,1])
    # print(len(train_x))
    # print(len(train_y))
    # print(train_x)
    # print(train_y)
    # resetting underlying graph data
    # ops.reset_default_graph()

    # Building neural network
    net = tflearn.input_data(shape=[None, len(train_x[0])])
    net = tflearn.fully_connected(net, 10)
    net = tflearn.fully_connected(net, 10)
    net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
    net = tflearn.regression(net)

    # Defining model and setting up tensorboard
    model = tflearn.DNN(net)
    # model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')

    # Start training
    model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
    model.save('resources/models/tflearn/model.tflearn')
    pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open( "resources/pickles/training_data_pkl", "wb" ) )
    print('Model Train SUCESSFULLY!')
            
if __name__ == '__main__':
    main()
