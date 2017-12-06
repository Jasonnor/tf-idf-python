import jieba
from operator import itemgetter

class tf_idf:
    def __init__(self):
        self.weighted = False
        self.documents = []
        self.corpus_dict = {}

    def add_document(self, doc_name, list_of_words):
        # building a dictionary
        doc_dict = {}
        for w in list_of_words:
            doc_dict[w] = doc_dict.get(w, 0.) + 1.0
            self.corpus_dict[w] = self.corpus_dict.get(w, 0.0) + 1.0

        # normalizing the dictionary
        length = float(len(list_of_words))
        for k in doc_dict:
            doc_dict[k] = doc_dict[k] / length

        # add the normalized document to the corpus
        self.documents.append([doc_name, doc_dict])

    def similarities(self, list_of_words):
        # building the query dictionary
        query_dict = {}
        for w in list_of_words:
            query_dict[w] = query_dict.get(w, 0.0) + 1.0

        # normalizing the query
        length = float(len(list_of_words))
        for k in query_dict:
            query_dict[k] = query_dict[k] / length

        # computing the list of similarities
        sims = []
        for doc in self.documents:
            score = 0.0
            doc_dict = doc[1]
            for k in query_dict:
                if k in doc_dict:
                    score += (query_dict[k] / self.corpus_dict[k]) + (
                      doc_dict[k] / self.corpus_dict[k])
            sims.append([doc[0], score])

        return sims


def set_stop_words(self, stop_words_path):
    abs_path = _get_abs_path(stop_words_path)
    if not os.path.isfile(abs_path):
        raise Exception("jieba: file does not exist: " + abs_path)
    content = open(abs_path, 'rb').read().decode('utf-8')
    for line in content.splitlines():
        self.stop_words.add(line)

if __name__ == "__main__":
    stop_words = set(())
    content = open('./dictionary/stop_words.txt', 'rb').read().decode('utf-8')
    for line in content.splitlines():
        stop_words.add(line)

    topK = 20
    file_name = '../data/笑傲江湖/01.txt'
    content = open(file_name, 'rb').read()
    words = jieba.lcut(content)
    freq = {}
    for w in words:
        if len(w.strip()) < 2 or w.lower() in stop_words:
            continue
        freq[w] = freq.get(w, 0.0) + 1.0
    total = sum(freq.values())

    print('、'.join(words))

    # for k in freq:
    #     freq[k] *= idf_freq.get(k, median_idf) / total

    tags = sorted(freq.items(), key=itemgetter(1), reverse=True)
    print(tags[:topK])

    # table = tf_idf()
    # table.add_document("foo", ["a", "b", "c", "d", "e", "f", "g", "h"])
    # print(table.similarities(["a", "b", "c"]))
