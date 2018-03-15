fo = open('./data/svm-data/HKIB_train.txt','w',encoding='utf-8')

for i in range(5):
    filename = "./data/svm-data/HKIB-20000_00" + str(i+1) + ".txt"
    f = open(filename, 'r', encoding='utf-8')

    strs = f.read()
    tmps = strs.split("@DOCUMENT\n")
    count=1
    for tmp in tmps:
        if count is 1:
            count=0
            continue


    f.close()
fo.close()
