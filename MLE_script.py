import numpy as np

from nltk.tokenize import word_tokenize
from collections import defaultdict
from collections import Counter
from numpy.random import choice 

with open('book text/1080.txt', encoding='utf-8') as text_file:
    content = text_file.read()
    content = content.replace('\\n', '\n').replace('\\r', '\r')
    words = word_tokenize(content)
   
#Taking this from ICE 9   
class Bigram():
    def __init__(self):
        self.bigram_counts = defaultdict(Counter)
        self.unigram_counts = Counter()
        self.context = defaultdict(Counter)
        self.token_count = 0
        self.vocab_count = 0
        
    def get_counts(self, sentence):
        for word in sentence[1:]:
            self.unigram_counts[word] += 1
                    
        bigram_list = zip(sentence[:-1], sentence[1:])
        for bigram in bigram_list:
            self.bigram_counts[bigram[0]][bigram[1]] += 1
            self.context[bigram[1]][bigram[0]] += 1
                    
        self.token_count = sum(self.unigram_counts.values())
        self.vocab_count = len(self.unigram_counts.keys())
        
    def generate_sentence(self, start_word):
        current_word = start_word
        sentence = []
        for i in range(1, 30):
            prev_word = current_word
            prev_word_counts = self.bigram_counts[prev_word]
            
            bigram_probs = np.zeros(len(prev_word_counts))
            total_counts = float(sum(prev_word_counts.values()))
            j = 0
            maximum = 0
            max_index = 0
            for word in prev_word_counts:
                if prev_word_counts[word]/total_counts > maximum:
                    maximum = prev_word_counts[word]/total_counts
                    max_index = j
                bigram_probs[j] = (prev_word_counts[word] / total_counts)
                j += 1
            
            one_hot_probs = np.zeros(len(prev_word_counts))
            one_hot_probs[max_index] = 1
            
            current_word = choice(list(prev_word_counts.keys()), p=one_hot_probs)
            sentence.append(current_word)
            
        sentence = " ".join(sentence)
        return sentence
        
modest_proposal_bigram = Bigram()
modest_proposal_bigram.get_counts(words)

generated_text = modest_proposal_bigram.generate_sentence('one')
print(generated_text)