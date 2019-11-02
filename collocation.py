import re
import string
import sys
coll_set = open("C:/Users/priya/Downloads/Collocations.txt")

try:
    f = open("C:/Users/priya/Downloads/Collocations.txt")
except IOError:
    print("Sorry, I could not find the file", sys.argv[1])
    print("Please try again.")
    sys.exit()

filecontents = f.read()


bigrams = {}
words_punct = filecontents.split()

words = [ w.strip(string.punctuation) for w in words_punct ]
print(words)

for index, word in enumerate(words):
    if index < len(words) - 1:
        w1 = words[index]
        w2 = words[index + 1]
        bigram = (w1, w2)

        if bigram in bigrams:
            bigrams[bigram] = bigrams[bigram] + 1
        else:
            bigrams[bigram] = 1

sorted_bigrams = sorted(bigrams.items(), key = lambda pair:pair[1], reverse = True)

for bigram, count in sorted_bigrams:
   print(bigram, ":", count)

unigrams ={}
words_punct = filecontents.split()
words = [ w.strip(string.punctuation) for w in words_punct ]
print(words)

for index, word in enumerate(words):
    if index < len(words) - 1:
        w3 = words[index]
        unigram = (w3)

        if unigram in unigrams:
            unigrams[unigram] = unigrams[unigram]
        w3 = words[index]
        unigram = (w3)
import math

def gf(x):
    #Play with these values to adjust the error of the approximation.

    upper_bound=100.0
    resolution=1000000.0

    step=upper_bound/resolution

    val=0
    rolling_sum=0

    while val<=upper_bound:
        rolling_sum+=step*(val**(x-1)*2.7182818284590452353602874713526624977**(-val))
        val+=step

    return rolling_sum

def ilgf(s,z):
    val=0

    for k in range(0,100):
        val+=(((-1)**k)*z**(s+k))/(math.factorial(k)*(s+k))
    return val

def chisquarecdf(x,k):
    return 1-ilgf(k/2,x/2)/gf(k/2)

def chisquare(observed_values,expected_values):
    test_statistic = 0
    chi_sq = open("C:/Users/priya/Downloads/Collocations.txt")
    for observed, expected in zip(observed_values, expected_values):
        test_statistic+=(float(observed)-float(expected))**2/float(expected)

    df=len(observed_values)-1

    return test_statistic, chisquarecdf(test_statistic,df)

#print(chisquare(observed_values, expected_values))

from collections import Counter
from math import log

corpus = open("C:/Users/priya/Downloads/Collocations.txt")
f = corpus.readlines()

def gen_bigrams(data, window_size=2):
    for i in range(len(data)):
        window = data[i: i + window_size]

        if len(window) < 2:
            break

        w = window[0]
        for next_word in window[1:2]:
            yield (w, next_word)


def construct_vocab(data):
    vocab = Counter()

    for (w1, w2) in gen_bigrams(data, window_size=2):  # count 1gram & 2gram
        vocab.update([w1, w2, (w1, w2)])
    return vocab


def calc_pmi(vocab):
    det = sum(vocab.values())

    for (w1, w2) in filter(lambda el: isinstance(el, tuple), vocab):
        p_a, p_b = float(vocab[w1]), float(vocab[w2])
        p_ab = float(vocab[(w1, w2)])

        yield (w1, w2, log((det * p_ab) / (p_a * p_b), 2))


gen_bigrams(f, 2)
voca = construct_vocab(f)

for (w1, w2, pmi) in calc_pmi(voca):
    print("{}_{}: {:.3f}".format(w1, w2, pmi))
