import jieba
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
        content = open('../data/' + file_name, 'rb').read()
        words = jieba.lcut(content)

        # Build dictionary
        dictionary = {}
        for w in words:
            if len(w.strip()) < 2 or w.lower() in self.stop_words:
                continue
            dictionary[w] = dictionary.get(w, 0.0) + 1.0
            self.corpus[w] = 0.0

        # Get term frequency
        total = sum(dictionary.values())
        for k in dictionary:
            dictionary[k] /= total

        # Add tf to the corpus
        self.files[file_name] = dictionary

    def get_tf_idf(self, file_name, top_k):
        # Get inverse document frequency
        for w in self.corpus.keys():
            w_in_f = 1.0
            for dictionary in self.files:
                if w in dictionary:
                    w_in_f += 1.0
            if w in self.files[file_name]:
                self.corpus[w] = log(len(self.files) / w_in_f) * self.files[file_name][w]
        tags = sorted(self.corpus.items(), key=itemgetter(1), reverse=True)
        print(tags[:top_k])

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
        for doc in self.files:
            score = 0.0
            doc_dict = doc[1]
            for k in query_dict:
                if k in doc_dict:
                    score += (query_dict[k] / self.corpus[k]) + (
                      doc_dict[k] / self.corpus[k])
            sims.append([doc[0], score])

        return sims

if __name__ == "__main__":
    table = tf_idf()

    for x in range(1, 10):#41
        file_name = '笑傲江湖/' + str(x).zfill(2) + '.txt'
        table.add_file(file_name)

    table.get_tf_idf(file_name='笑傲江湖/02.txt', top_k=20)
