import json
'''
1.载入文件
2.查询语句处理
3.输出相关信息
'''
#----<set file path>----
postinglist_path = 'data/PostingList.json'
wordmap_path = 'data/WordMap.json'
doc_path = 'data/data.json'

class Searcher:
    def __init__(self):
        #---<open file>---
        with open(wordmap_path,'r',encoding="utf-8")as fp_wordmap:
            self.WordMap = json.load(fp_wordmap)
        fp_wordmap.close()
        with open(postinglist_path,'r',encoding="utf-8")as fp_postinglist:
            self.PostingList = json.load(fp_postinglist)
            self.PL_word_num = self.PostingList[0]
        fp_postinglist.close()
        with open(doc_path,'r',encoding="utf-8")as fp_doc:
            self.doc_info = json.load(fp_doc)
        self.all_doc_id=[]
        for box in self.doc_info:
            self.all_doc_id.append(box['id'])
        fp_doc.close()
        

    def bool_search(self ,query:str):
        #---<终止程序>---
        if query == "exit":
            exit(0)
        #---<开始查询语句处理>---
        self.token = query.replace('(', ' ( ').replace(')', ' ) ').split()
        self.ptr = 0
        self.token.append('$') #LL(1)语句终结符
        doc_ids =  self.E()[0]
        #---<输出相关信息>---
        lenth = len(doc_ids)
        if lenth == 0:
            print('<0>found nothing')
        else:
            print('<'+str(lenth)+'>Here is the result')
            for doc_id in doc_ids:
                for box in self.doc_info:
                    if str(doc_id) == box['id']:
                        print("|>"+str(lenth)+"<|")
                        lenth = lenth - 1
                        #名字
                        print('名字：'+box['name'])
                        #类型
                        sentences = box['info'].split('\n')
                        for i in range(len(sentences)-1,-1,-1):
                            if "类型" in sentences[i]:
                                print(sentences[i])
                                break
                        #评分
                        sentences = box['rating'].split('\n')
                        for i in range(len(sentences)):
                            if "." in sentences[i]:
                                print("评分："+sentences[i])
                                break
                        #简介
                        print("简介："+box['intro'].replace('\n','').replace(' ','').strip())

        print()

    #-----<查询语句处理>---
    '''
    LL(1)
        E-> T OR E | T
        T-> F AND T | F
        F-> NOT F | (E) | word | nil 
        //这里nil是保证在查询"A OR B"时，若B为空，依旧可以正确返回A
        //在分析E时先判断是否有OR
    '''
    def E(self):
        T = self.T()
        if(self.token[self.ptr]=='OR'):
            self.ptr += 1
            E = self.E() 
            if T[1]==True or E[1]==True:
                return (Searcher.OR(T[0], E[0]), True)
            else:
                return ([],False)
        elif(T[1] == False):
            return([], False)
        else:
            return(T[0], True)

    def T(self):
        F = self.F()
        if(F[1] == False):
            return([], False)
        elif(self.token[self.ptr]=='AND'):
            self.ptr += 1
            T = self.T()
            return (Searcher.AND(F[0], T[0]), True)
        else:
            return (F[0], True)

    def F(self): 
        if(self.token[self.ptr]=='NOT'):
            self.ptr += 1
            F = self.F()
            return (self.NOT(F[0]), True)
        elif(self.token[self.ptr]=='('):
            self.ptr += 1
            E = self.E()
            self.ptr += 1
            return(E[0], True)
        else:
            list = self.GetList(self.token[self.ptr])
            self.ptr += 1
            #----<还原PL中id>---
            if len(list) > 1:
                first_id=str(list[0])
                for i in range(1,len(list)):
                    next_id_gap=str(list[i]) 
                    real_id=int(next_id_gap)+int(first_id)
                    list[i]=str(real_id)
                return (list, True)
            elif len(list) == 1:
                return (list, True)
            else: return ([],False) #nil->[]

    #---<该函数得到相关的原始倒排表，在self.F()中被引用>---
    def GetList(self, word):
        if word in self.WordMap:    
            word_id = self.WordMap[word]
            get_list = self.PostingList[word_id]
        else:
            print('<!>This word was not found: '+word)
            get_list=[]
        #return [x[0] for x in pre_list]
        return get_list

    #----<以下是NOT AND OR>---
    def NOT(self, L):
        #求L中的id的补集
        return [x for x in self.all_doc_id if x not in L]

    def AND(L1, L2):
        result = []
        for i in range(len(L1)):
            for j in range(len(L2)):
                if L2[j] not in result and L2[j] == L1[i]:
                    result.append(L2[j])
        return result

    def OR(L1: list, L2: list) -> list:
        result = []
        for i in range(len(L1)):
            result.append(L1[i])
        for j in range(len(L2)):
            if L2[j] not in result:
                result.append(L2[j])
        return result

if __name__ == '__main__':
    while True:
        query = input('[Bool Search]>>  ')
        S = Searcher()
        S.bool_search(query)
        #在bool_search()中匹配终止语句
