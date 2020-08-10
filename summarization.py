# -*- coding: utf-8 -*-

""" IMPORTS """

import re
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

""" FONCTION DE TOKENISATION """

def tokenize_sentences(text, f):
    
    # Changement des séparateurs de phrases
    punct_0 = re.compile(r'[ ]*\.+[ \|!?\n]+')
    text = re.sub(punct_0, '. ', text)
    punct_1 = re.compile(r'[ ]*[\|!?\n]+[ ]*')
    text = re.sub(punct_1, '. ', text)
    
    # Tokenisation pour séparer correctement les unités
    token = f.pretokenize(text)
    text = " ".join(token)
    
    # Changement des séparateurs de phrases
    point = re.compile(r'(\. | \.)')
    text = re.sub(point, ' | ', text)
    list_sentences = text.split('|')
    
    return list_sentences

""" OUTIL DE RESUME """

class SimilaritySummary(object):
    
    def __init__(self, f):
        self.f = f
        
    def sentence_similarity(self, sent1, sent2):
     
        sent1 = [w.lower() for w in sent1]
        sent2 = [w.lower() for w in sent2]
     
        all_words = list(set(sent1 + sent2))
     
        vector1 = [0] * len(all_words)
        vector2 = [0] * len(all_words)
     
        # build the vector for the first sentence
        for w in sent1:
            vector1[all_words.index(w)] += 1
     
        # build the vector for the second sentence
        for w in sent2:
            vector2[all_words.index(w)] += 1
     
        return 1 - cosine_distance(vector1, vector2)
     
    def build_similarity_matrix(self, sentences):
        # Create an empty similarity matrix
        similarity_matrix = np.zeros((len(sentences), len(sentences)))
     
        for idx1 in range(len(sentences)):
            for idx2 in range(len(sentences)):
                if idx1 == idx2: #ignore if both are same sentences
                    continue 
                similarity_matrix[idx1][idx2] = self.sentence_similarity(sentences[idx1], sentences[idx2])
    
        return similarity_matrix
    
    def generate_summary(self, text, preprocessed_text, top_n=5):
        
        summarize_text = []
        
        # Step 1 - Tokenize and clean sentences
        ss = preprocessed_text.split(' | ')
        sentences = []
        for e in ss:
            if e == '':
                sentences.append(" ")
            else:
                sentences.append(e.strip(' '))

        # Supression des éléments indésirables en bout de phrases, et des heures
        ss_copy = tokenize_sentences(text.lower(),self.f)
        
        sentences_copy = []
        
        for s in ss_copy:
            sentences_copy.append(s.strip(',;:.?!§ '))

        # Si le résumé demande plus de phrases que le texte, on prend la taille du texte
        if len(sentences)<top_n:
            top_n = len(sentences)
            
        # Step 2 - Generate Similary Martix across sentences
        sentence_similarity_martix = self.build_similarity_matrix(sentences)
    
        # Step 3 - Rank sentences in similarity martix
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
        scores = nx.pagerank(sentence_similarity_graph, max_iter = 100)
        # la variable "scores" est un dictionnaire avec le rang de la phrase en clé et son score en valeur
        
        # Step 4 - Sort the rank and pick top sentence
        ranked_sentence_numbers = []
        for k, v in sorted(scores.items(), key=lambda x: x[1], reverse = True):
            if len(ranked_sentence_numbers)<top_n:
                ranked_sentence_numbers.append(k)
            else:
                break
        ranked_sentence_numbers.sort()
        
        for number in ranked_sentence_numbers:
            summarize_text.append(sentences_copy[number])
    
        # Step 5 - Offcourse, output the summarize text
        return " | ".join(summarize_text)
    