def category_dictionary():
    f=open('./data/svm-data/hkib.categories','r',encoding='utf-8')
    for i in range(3):
        f.readline()
    lines = f.readlines()
    dic={}
    for line in lines:
        if '-' not in line:
            tmp = line.split('/')
            if tmp[1] in dic:
                dic[tmp[1]] += int(tmp[0])
            else:
                dic[tmp[1]] = int(tmp[0])
    f.close()
    return (dic)

fi = open('./data/svm-data/pos_train.txt','r',encoding='utf-8')
strings = fi.read()
fi.close()

flag=1
string_list = []
category_list = []
word_list = {}
word_with_category = {}
word_count=0
category_count = category_dictionary()

for string in strings.split('@DOCUMENT'):
    if flag == 1:
        flag=0
        continue
    string_list.append(string.split('#TEXT')[0])
    category = (string.split("#CAT'03:")[1].split('/')[1])
    category_list.append(category)
    string_set = set(string.split('#TEXT')[1].split())
    string_set = list(string_set)
    #in form of category_word, dictionary save
    for tmp in string_set:
        if category + "_" + tmp in word_with_category:
            word_with_category[category + "_" + tmp] += 1
        else:
            word_with_category[category + "_" + tmp] = 1

    for tmp in string.split('#TEXT')[1].split():
        if tmp not in word_list:
            word_list[word_count]=tmp
            word_count+=1
#print(len(word_list))
#print(category_count['경제'])
category_name = ['건강과 의학','경제','과학','교육','문화와 종교','사회','산업','여가생활']

#calculating kai_square value of each word
#import bisect
from tqdm import tqdm
kai_square_t_c = {}
kai_square_tmp = []
#kai_square_to_idx = {}
fi = open('./data/svm-data/kai_square_list.txt','wb')
for i in range(8):
    for j in tqdm(range(len(word_list))):
        if category_name[i] + '_' + word_list[j] in word_with_category:
            A = word_with_category[category_name[i] + '_' + word_list[j]]
        else:
            A=0
        B = category_count[category_name[i]] - A
        #calculating C
        ctmp=0
        for k in range(8):
            if category_name[k] + '_' + word_list[j] in word_with_category:
                ctmp+=word_with_category[category_name[k] + '_' + word_list[j]]
        C = ctmp - A
        D = 20000 - A - B - C
        _kai_sqaure = (A*D-B*C)*(A*D-B*C) / ((A+C)*(B+D)*(A+B)*(C+D)+1)
        kai_square_t_c[category_name[i] + '_' + word_list[j]] = _kai_sqaure
        #kai_square_tmp[len(word_list) * i + j] = _kai_square

import operator
d_descending = sorted(kai_square_t_c.items(), key=operator.itemgetter(1), reverse=True)
import pickle
pickle.dump(d_descending, fi)
fi.close()

