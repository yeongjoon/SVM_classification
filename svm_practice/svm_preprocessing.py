#-*- coding: utf-8 -*-

def category_dictionary():
    f = open('./data/svm-data/hkib.categories','r',encoding='utf8')
    for i in range(3):
        f.readline()
    lines = f.readlines()
    dic = {}
    for line in lines:
        if '-' not in line:
            tmp = line.split('/')
            if tmp[1] in dic:
                dic[tmp[1]] += int(tmp[0])
            else:
                dic[tmp[1]] = 0
    return (dic)
    f.close()

""" first save some words and pos tags in the dictionary 
    only used NNP, and NNG """
import re
pos_dic = {}
################################something happend(pos_data2)########
f = open("./data/svm-data/kai_pos_data.txt",'r',encoding="utf-8")
strs = f.read()
f.close()
tmps = strs.split("@DOCUMENT\n")
flag=1
count=0
loop_count=0
ftmp = open("./data/svm-data/word_list.txt",'w',encoding="utf-8")
for tmp in tmps:
    if flag is 1:
        flag=0
        continue
    word_with_tags = tmp.split('#TEXT')[1]
    for item in word_with_tags.split():
        loop_count +=1
        if item not in pos_dic:
            if bool(re.search('NNG',item)) is True or bool(re.search("NNP",item)) is True or bool(re.search('NNB',item)) is True or bool(re.search('XR',item)) is True:
                ########revised
                #if item.split('_')[0] not in pos_dic:
                #    pos_dic[item.split('_')[0]] = count
                #    count += 1
                pos_dic[item] = count
                count+=1
for k, v in pos_dic.items():
    ftmp.write(k)
    ftmp.write("\n")

print("There are ",len(pos_dic), "POS tags in the text")
print(loop_count)
""" only nnp, and nng"""
#for i in pos_dic.copy():
#    if bool(re.search('NNG',i)) is False and bool(re.search("NNP",i)) is False:
#        pos_dic.pop(i)
#pos_dic = tmp_dic
#print(pos_dic["*_SW"])
#for k, v in pos_dic.items():
#    print (k,v)
#print(count)
"""
flag=1
count=0

X_data = []
Y_label = []

for tmp in tmps:
    if flag is 1:
        flag=0
        continue
    word_with_tags = tmp.split('#TEXT')[1]
    pos_list = []
    for item in word_with_tags.split():
        if bool(re.search('NNG',item)) is True or bool(re.search("NNP",item)) is True:
            pos_list.append(item)
    category = tmp.split("#CAT'03:")[1].split("#CAT'07:")[0].split("/")[1]
    X_data.append(word_with_tags)
    Y_label.append(category)

from sklearn.feature_extraction.text import TfidfVectorizer
X_data = TfidfVectorizer().fit_transform(X_data)
"""
#print("There are ",len(pos_dic), "POS tags in the text")


""" now we have to preprocess for sklearn """
X_data = []
Y_label = []
flag=1
for tmp in tmps:
    if flag is 1:
        flag=0
        continue
    #used komoran and made it into proper format.
    word_with_tags = (tmp.split('#TEXT'))[1]
    feature_list = []
    #feature_list = [0 for _ in range(len(pos_dic))]
    for i in range(len(pos_dic)):
        feature_list.append(0)
    category = tmp.split("#CAT'03:")[1].split("#CAT'07:")[0].split("/")[1]
    for item in word_with_tags.split():
        if item in pos_dic:
            feature_list[pos_dic[item]]+=1 #not bag of words, but tfidf

    X_data.append(feature_list)
    Y_label.append(category)

cross_validation_k = 0.1
""" Cross Validation """
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer #For tfidf
X_train, X_test, y_train, y_test = train_test_split(X_data, Y_label, test_size=cross_validation_k, random_state=42)

X_train = TfidfTransformer(smooth_idf=True).fit_transform(X_train)
#X_train, X_test, y_train, y_test = train_test_split(X_data, Y_label, test_size=cross_validation_k)
from sklearn.svm import LinearSVC
#X_train = TfidfTransformer(smooth_idf=True).fit_transform(X_train)

clf = LinearSVC(random_state=42)
clf.fit(X_train, y_train)
#print(clf.coef_)
filename = './data/svm-data/output' + str(cross_validation_k * 100) + '%.txt'
fo = open(filename,'w',encoding='utf-8')
fo.write("Accuracy: ")
fo.write(str(clf.score(X_test, y_test)))
fo.write('\n')
fo.close()

