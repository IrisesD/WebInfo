import jieba
import synonyms

stop_file="dict/cn_stopwords.txt"
add_word_file="dict/add_word_list.txt"

class Sparse:
    def __init__(self,text):
        self.document = text

    def rm_extra_symbol(self):
        self.document = self.document.replace('\r','').replace('\n','').replace(' ','').replace('\t','').strip()

    def get_words(self):
        #----<load add list>----
        jieba.load_userdict(add_word_file)
        #----<seg in jieba Full Mode>----
        seg_list = jieba.cut(self.document, cut_all=True)
        #----<rm stop words>----
        with open(stop_file, 'r', encoding='utf-8') as s_f:
            stopword_list = [word.strip('\n') for word in s_f.readlines()]
        s_f.close()
        s_words=[]
        for w in seg_list:
            if w not in stopword_list:
                s_words.append(w)
        #----<Merge synonyms>---
        self.words=[]
        for i in range(len(s_words)):
            if s_words[i] not in self.words:
                self.words.append(s_words[i])
            for j in range(i+1,len(s_words)):
                if s_words[j] not in self.words and synonyms.compare(s_words[i], s_words[j], seg=False) < 0.7:
                    self.words.append(s_words[j])
    
    #def search_words(self):
        
        
    def sparse(self):
        self.rm_extra_symbol()
        self.get_words()
        return self.words
