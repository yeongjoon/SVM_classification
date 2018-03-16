#-*- coding: utf-8 -*-

""" first save some words and pos tags in the dictionary 
    only used NNP, and NNG """
import re
pos_dic = {}
################################something happend(pos_data2)########
f = open("./data/svm-data/kai_pos_train.txt",'r',encoding="utf-8")
strs = f.read()
f.close()
tmps = strs.split("@DOCUMENT\n")
flag=1
count=0
loop_count=0
for tmp in tmps:
    if flag is 1:
        flag=0
        continue
    word_with_tags = tmp.split('#TEXT')[1]
    category = tmp.split("#CAT'03:")[1].split("#CAT'07:")[0].split("/")[1]
    for item in word_with_tags.split():
        loop_count +=1
        if item not in pos_dic:
            if bool(re.search('NNG',item)) is True or bool(re.search("NNP",item)) is True:
                ########revised
                #if item.split('_')[0] not in pos_dic:
                #    pos_dic[item.split('_')[0]] = count
                #    count += 1
                pos_dic[item] = count
                count+=1

print("There are ",len(pos_dic), "POS tags in the text")
print(loop_count)

##########################################revised
import pickle
#from sklearn.model_selection import train_test_split
ftmp = open("./data/svm-data/kai_square_dict.txt",'rb')
pos_dic2 =  pickle.load(ftmp)
ftmp.close()
###################################################
print(len(pos_dic2))
f = open("./data/svm-data/pos_test.txt","r",encoding='utf-8')
strs = f.read()
f.close()
tmps=strs.split("@DOCUMENT\n")

#For test data
X_test = []
y_test = []
flag=1
for tmp in tmps:
    if flag is 1:
        flag=0
        continue
    word_with_tags = (tmp.split('#TEXT'))[1]
    feature_list_test = []
    #feature_list = [0 for _ in range(len(pos_dic))]
    for i in range(len(pos_dic)):
        feature_list_test.append(0)
    category = tmp.split("#CAT'03:")[1].split("#CAT'07:")[0].split("/")[1]
    for item in word_with_tags.split():
        if category + '_' + item in pos_dic2:
            if item in pos_dic:
                feature_list_test[pos_dic[item]]+=1 #not bag of words, but tfidf

    X_test.append(feature_list_test)
    y_test.append(category)

""" only nnp, and nng"""
f3 = open('./data/svm-data/pos_train.txt','r',encoding='utf-8')
strs = f3.read()
f3.close()
tmps = strs.split("@DOCUMENT\n")


#for train data
X_train = []
y_train = []
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
        if category + '_' + item in pos_dic2:
            if item in pos_dic:
                feature_list[pos_dic[item]]+=1 #not bag of words, but tfidf

    X_train.append(feature_list)
    y_train.append(category)

#print(X_train[:1], X_test[:1])
#print(y_train[:5], y_test[:5])
#cross_validation_k = 0.1
#""" Cross Validation """
#from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer #For tfidf
#X_train, X_test, y_train, y_test = train_test_split(X_data, Y_label, test_size=cross_validation_k, random_state=42)

from sklearn.svm import LinearSVC
X_train = TfidfTransformer(smooth_idf=True).fit_transform(X_train)
X_test = TfidfTransformer(smooth_idf=True).fit_transform(X_test)

clf = LinearSVC(random_state=42)
clf.fit(X_train, y_train)
#print(clf.predict(X_test[1]))
#print(clf.coef_)
import sys

filename = './data/svm-data/output.txt'
if len(sys.argv) is 2:
    filename = './data/svm-data/output' + sys.argv[1] + '.txt'
fo = open(filename,'w',encoding='utf-8')
fo.write("Accuracy: ")
fo.write(str(clf.score(X_test, y_test)))
fo.write('\n')
fo.close()

