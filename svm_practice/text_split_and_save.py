whole_list = []
fi = open('./data/svm-data/pos_data3.txt','r',encoding='utf-8')
strs = fi.read()
fi.close()
tmps = strs.split("@DOCUMENT\n")
flag=1
for tmp in tmps:
    if flag is 1:
        flag=0
        continue
    whole_list.append(tmp)

from sklearn.model_selection import train_test_split
train_list, test_list = train_test_split(whole_list, test_size=0.1, random_state=42)

ftrain = open('./data/svm-data/pos_train.txt','w',encoding='utf-8')

for line in train_list:
    ftrain.write("@DOCUMENT\n")
    ftrain.write(line)
    ftrain.write('\n')

ftest = open('./data/svm-data/pos_test.txt','w',encoding='utf-8')
for line in test_list:
    ftest.write("@DOCUMENT\n")
    ftest.write(line)
    ftest.write("\n")

ftrain.close()
ftest.close()
