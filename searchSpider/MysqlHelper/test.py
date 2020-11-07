import MysqlHelper
import datetime
import time
msh = MysqlHelper.MysqlHelper(host="localhost", username="root", password="123456", db="topic_evolution",
                              charset="utf8", port=3306)
msh.connect()
sql = "select * from disease"
all_items = msh.get_all(sql)
print(len(all_items))
def replace_char(string,char,index):
    string = list(string)
    string[index] = char
    return ''.join(string)

for each in all_items:
    id = each[3]
    time_pass = str(each[1])
    x = replace_char(time_pass,'2',2)
    x = replace_char(x,'0',3)
    time1 = datetime.datetime.strptime(x,"%Y-%m-%d %H:%M:%S")
    #print(time1)
    #print(type(time1))
    sql = "update disease set time = ' " + x +"'where url = '" + id + "'"
    msh.update(sql)


import jieba


def preprocess(path):
    text = ""
    fenci = open(path, "r", encoding="utf-8").read()
    jieba.load_userdict("./dict.txt")
    seg = jieba.cut(fenci)
    # fenci = "/".join(fenci)
    print(' '.join(seg))


print(preprocess('./1.txt'))


import MysqlHelper
import datetime
import time
msh = MysqlHelper.MysqlHelper(host="localhost", username="root", password="123456", db="topic_evolution",
                              charset="utf8", port=3306)
msh.connect()
sql = "delete from disease where  LENGTH(trim(article))=0"
msh.delete(sql)