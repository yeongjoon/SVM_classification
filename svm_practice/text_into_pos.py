from konlpy.tag import Komoran
komoran = Komoran()

fo = open("./data/svm-data/pos_data3.txt",'w',encoding="utf-8")
item_dic = {}
for i in range(5):
    filename = "./data/svm-data/HKIB-20000_00" + str(i+1) + ".txt"
    f = open(filename,'r',encoding="utf-8")

    strs = f.read()
    tmps = strs.split("@DOCUMENT\n")
    print(len(tmps))
    count=1
    for tmp in tmps:
        if count is 1:
            count = 0
            continue
        #print (tmp.split(':')[1].split('\n'))[0]
        #print(tmp[1].split('#TEXT')[0])
        """extracting categories and the text"""
        #print(tmp.split("#CAT'03:")[1].split("#CAT'07:")[0].split("/")[1])
        fo.write("@DOCUMENT\n")
        fo.write(tmp.split('#TEXT')[0])
        fo.write("#TEXT\n")
        #_pos = komoran.pos(tmp.split('#TEXT')[1].split(':')[1].split('<KW>')[0].replace('\n','').replace(',',' '))
        for a in tmp.split('#TEXT  :')[1].split('<KW>')[0].replace('\n','').replace(',',' ').split('.'):
            _pos = komoran.pos(a)
            for item in _pos:
                if item[1] == 'NNG' or item[1] == 'NNP':
                    fo.write(item[0] + "_" + item[1])
                    fo.write("\n")
        #added here
        """
        if tmp.count('<KW>') is 1:
            _pos2 = komoran.pos(tmp.split('#TEXT')[1].split('<KW>')[1].replace('\n',' '))
            for item in _pos2:
                fo.write(item[0] + "_" + item[1])
                fo.write("\n")
        """
        fo.write("\n")
    f.close()
    print ("hello")
fo.close()


