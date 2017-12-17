import jieba
import os
from math import log
from operator import itemgetter


class tf_idf:
    def __init__(self):
        self.files = {}
        self.corpus = {}
        self.stop_words = set(())
        content = open('./dictionary/stop_words.txt', 'rb').read().decode('utf-8')
        for line in content.splitlines():
            self.stop_words.add(line)

    def add_file(self, file_name):
        # Load data and cut
        content = open(file_name, 'rb').read()
        words = jieba.cut(content)

        # Build dictionary
        dictionary = {}
        for w in words:
            if len(w.strip()) < 2 or w.lower() in self.stop_words:
                continue
            dictionary[w] = dictionary.get(w, 0.0) + 1.0
            self.corpus[w] = self.corpus.get(w, 0.0) + 1.0

        # Get term frequency
        total = sum(dictionary.values())
        for k in dictionary:
            dictionary[k] /= total

        # Add tf to the corpus
        self.files[file_name] = dictionary

    def get_tf_idf(self, file_name, top_k):
        # Get inverse document frequency
        tf_idf_of_file = {}
        for w in self.corpus.keys():
            w_in_f = 1.0
            for f in self.files:
                if w in self.files[f]:
                    w_in_f += 1.0
            # Get tf-idf
            if w in self.files[file_name]:
                tf_idf_of_file[w] = log(len(self.files) / w_in_f) * self.files[file_name][w]
        # Top-K result of tf-idf
        tags = sorted(tf_idf_of_file.items(), key=itemgetter(1), reverse=True)
        return tags[:top_k]

    def similarities(self, list_of_words):
        # Building the query dictionary
        query_dict = {}
        for w in list_of_words:
            query_dict[w] = query_dict.get(w, 0.0) + 1.0

        # Normalizing the query
        length = float(len(list_of_words))
        for k in query_dict:
            query_dict[k] = query_dict[k] / length

        # Get the list of similarities
        sims = []
        for f in self.files:
            score = 0.0
            for k in query_dict:
                if k in self.files[f]:
                    score += (query_dict[k] / self.corpus[k]) + (self.files[f][k] / self.corpus[k])
            sims.append([f, score])

        return sorted(sims, key=itemgetter(1), reverse=True)

