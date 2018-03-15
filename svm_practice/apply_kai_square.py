
ftmp = open('./data/svm-data/kai_square_list.txt','rb')
import pickle
kai_square_list = pickle.load(ftmp)
ftmp.close()

import sys

if len(sys.argv) is 1:
    print ("Error! No input of percentage to slice")
    sys.exit(1);

percentage_to_cut = float(sys.argv[1]) / 100.0
length_to_cut = int(len(kai_square_list) * percentage_to_cut)
sliced_kai_square_list = kai_square_list[:length_to_cut]
kai_dict = dict(sliced_kai_square_list)

del(kai_square_list)
del(sliced_kai_square_list)

print('"kai_pos_data.txt" has been created with top ',int(percentage_to_cut*100),'% of the data.')
#print(kai_dict)
#print(bool('사회_수사_NNG' in kai_dict))
fi = open('./data/svm-data/pos_data3.txt','r',encoding='utf-8')

fo = open('./data/svm-data/kai_pos_data.txt','w',encoding='utf-8')

strs = fi.read()
tmps = strs.split('@DOCUMENT\n')
fi.close()
flag=1
for tmp in tmps:
    if flag==1:
        flag=0
        continue
    category = tmp.split("#CAT'03:")[1].split('/')[1]
    fo.write("@DOCUMENT\n")
    fo.write(tmp.split('#TEXT')[0])
    fo.write("#TEXT\n")
    for word in tmp.split('#TEXT\n')[1].split():
        full_word = category + '_' + word
        #print(full_word)
        if full_word in kai_dict:
            #print(1)
            fo.write(word)
            fo.write('\n')
    fo.write('\n')
fo.close()
