import os
from django.conf import settings
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import WordPunctTokenizer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
from nltk.classify import *
from nltk.probability import DictionaryProbDist
from sklearn.svm.sparse import LinearSVC
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import sys
import urllib2
import random
import numpy as np 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.multiclass import OneVsRestClassifier
from sklearn.feature_extraction.text import CountVectorizer
import cPickle
def extract_words(text):

    '''
   here we are extracting features to use in our classifier. We want to pull all the words in our input
   porterstem them and grab the most significant bigrams to add to the mix as well.
   '''
 
    stemmer = PorterStemmer()
 
    tokenizer = WordPunctTokenizer()
    tokens = tokenizer.tokenize(text)
    bigram_finder = BigramCollocationFinder.from_words(tokens)
    bigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 500)
    
    for bigram_tuple in bigrams:
        x = "%s %s" % bigram_tuple
        tokens.append(x)
 
    result =  [stemmer.stem(x.lower()) for x in tokens if x not in stopwords.words('english') and len(x) > 1]
#    print result
    return result
 
def get_feature(word):
    return dict([(word, True)])
 
 
def bag_of_words(words):
    return dict([(word, True) for word in words])
 
 
def create_training_dict(text, sense):
    ''' returns a dict ready for a classifier's test method '''
    tokens = extract_words(text)
    return [(bag_of_words(tokens), sense)]
 
 
 
def run_classifier_tests(classifier):
   testfiles = [{'food': 'foodtweets.txt'},
                {'company': 'training.txt'}]
   testfeats = []
   test2 = []
   for file in testfiles:
       for sense, loc in file.iteritems():
           print loc
           with open(loc) as infile:
               for line in infile:
                  testfeats = testfeats + create_training_dict(line, sense)
   test2 = brown.tagged_sents(categories='fiction') 
   #testfeats = testfeats + test2
   acc = accuracy(classifier, testfeats) * 100
   print '---------accuracy: %.2f%%' % acc
 
   sys.exit()
 
 
def training_set():
   # create our dict of training data
    texts = {}
    texts['food'] = "mainfood.txt"
    texts['company'] = 'company.txt'
    texts['books'] = 'books.txt'
    texts['music'] = 'music.txt'
    texts['technology']='tech.txt' 
    texts['religion']='religion.txt'
    texts['travel']='travel.txt'
    texts['hobbies']='hobbies.txt'
    texts['sports']='sports.txt'
    texts['coding']='coding.txt'
    texts['careers']='careers.txt' 
    texts['education']='education.txt'
    texts['people']='people.txt'
    texts['politics']='politics.txt' 
    texts['nature']='nature.txt'
     #holds a dict of features for training our classifier
    train_set = []
   #train_test2 = []
  # loop through each item, grab the text, tokenize it and create a training feature with it
    for sense, file in texts.iteritems():
       print "training %s " % sense
       f=open(file, 'r')
       text = f.read()
       # print text
       features = extract_words(text)
       train_set = train_set + [(get_feature(word), sense) for word in features]
#   classifier = NaiveBayesClassifier.train(train_set)
#pipeline = Pipeline([('tfidf', TfidfTransformer()),
 #                      ('chi2', SelectKBest(chi2, k=1000)),
  #                       ('nb', LogisticRegression())])
    classifier=SklearnClassifier( OneVsRestClassifier(LogisticRegression())).train(train_set)
    
    with open('my_dataset.pkl','wb') as fid: 
       cPickle.dump(classifier,fid)   
#   # uncomment out this line to see the most informative words the classifier will use
#classifier.show_most_informative_features(50)
   
   

   # uncomment out this line to see how well our accuracy is using some hand curated tweets
 #  run_classifier_tests(classifier) 
  

def train(line):
 tokens = bag_of_words(extract_words(line))
 f1=open(os.path.join(settings.MEDIA_ROOT, 'nltk/my_dataset.pkl'), 'r')
 classifier=cPickle.load(f1)
 f1.close()
 #cla
 print tokens
 decision = classifier.classify(tokens)
 labels  = classifier.prob_classify(tokens)
 #batch = classifier.batch_classify(tokens)
 #for b in batch:
 # print b
 print labels.samples()
 print "food     :%s" % labels.prob('food')
 print "books    : %s " %labels.prob('books')
 print "tech     : %s " %labels.prob('technology')
 print "music    : %s" %labels.prob('music')
 print "travel   :%s "%labels.prob('travel')
 print "sports   :%s"%labels.prob('sports') 
 print "company  : %s"  %labels.prob('company')
 print "coding   : %s" %labels.prob('coding')
 print "hobbies  : %s" %labels.prob('hobbies')
 print "careers  : %s" %labels.prob('careers')
 print "religion : %s" %labels.prob('religion')
 print "education :%s" %labels.prob('education')
 print "people    : %s" %labels.prob('people')
 print "politics  :%s " %labels.prob('politics')
 print "nature    :%s " %labels.prob('nature')
 print decision
#label_names = ['food', 'books','technology','music','travel','sports','company','coding','hobbies','careers','religion','education']
#predictions = [label_names[pred] for pred in classifier.predict(new_samples)]
 result = "%s - %s" % (decision,line)
 return decision
'''
choice = raw_input("is the decision correct?")
if choice == "no":
 filename = raw_input("enter the name of the file to which u want to enter")
 f = open(filename,"a")
 f.write("\n %s" %str(line))
 training_set()
 
'''