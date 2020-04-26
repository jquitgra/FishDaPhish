import math
import numpy as np
from textblob import TextBlob

def get_emailData(file):
    with open(file, "r") as infile:
        data = infile.read().replace('\n', ' ')
    body = data
    blob = TextBlob(body)
    tag_vec = []
    sentiments = []
    for tag in blob.tags:
        tag_vec.append(tag[1])   
    sentiments.append(blob.sentiment.polarity)
    sentiments.append(blob.sentiment.subjectivity)
    return tag_vec, sentiments

def get_tagVect(body):
    blob = TextBlob(body)
    tag_vec = []
    for tag in blob.tags:
        tag_vec.append(tag[1])
    return np.array(tag_vec)


def get_sentiment(body):
    blob = TextBlob(body)
    sentiments = []
    sentiments.append(blob.sentiment.polarity)
    sentiments.append(blob.sentiment.subjectivity)
    return sentiments