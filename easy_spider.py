#!/usr/bin/python3
# -*- coding: utf-8 -*-
#@Author  : laowantong001
#@Time    : 2021/11/4  10:30
#@Software: pycharm

import requests
import re
import os
from bs4 import BeautifulSoup
import time
from pyquery import PyQuery as pq
from PIL import Image  #pip install Pillow     python3的PIL模块都继承在Pillow里面了

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'Cookie':'UM_distinctid=17cdae743f16aa-0938793cf1215c-c791039-1fa400-17cdae743f259d; '
               'ecLm_2132_saltkey=Ze7NfYYw; ecLm_2132_lastvisit=1635759002; '
               'ecLm_2132_st_p=11288%7C1635938392%7C364af92757a1b7edb5e3a09ff2a1a2e0; '
               'ecLm_2132_visitedfid=39D2D38D36D46; ecLm_2132_viewid=tid_757; '
               'CNZZDATA1280328677=1254751082-1635758858-null%7C1635932433; '
               'ecLm_2132_st_t=11288%7C1635762884%7Cf47c1ab9e67029ec7b37367ba6bac795; '
               'ecLm_2132_forum_lastvisit=D_46_1635762642D_38_1635762884; ecLm_2132_home_diymode=1; '
               'ecLm_2132_seccodecSXWHM5z=25828.ea94e2cb5eefdbfc7f; '
               'ecLm_2132_ulastactivity=84afcEw2kexOVu8BbsKInhE5Huj0Wj9LRvPD4ppREFuGpLrAbTje; '
               'ecLm_2132_auth=1ea86%2F9q17jo3JjVS8EdtD2rU2h8gVUpzD8AYhMMpB48MNsY%2BFlpOLip4iLfhFlfTojhUGcokLMhNaPM'
               '%2FUNJM%2BM5Yw; ecLm_2132_nofavfid=1; ecLm_2132_sid=YS7b7W; '
               'ecLm_2132_lip=219.76.152.181%2C1635938142; ecLm_2132_lastact=1635938570%09misc.php%09patch; '
               'ecLm_2132_smile=1D1; ecLm_2132_seccodecSATCWgn=27749.bf6a93c158e5e78c7f; '
               'ecLm_2132_seccodecSeIMD8i=27759.9cf39e9a1cdd025960; '
               'ecLm_2132_seccodecSD0K7Z7=27901.a03fd9c65dea30ffb7; '
               'ecLm_2132_seccodecSsjwdzU=31443.972cb2d68cd6db2f67; '
               'ecLm_2132_seccodecSv977V5=32714.abb8e2235cf07ae3e8; '
               'ecLm_2132_seccodecSrV2XNO=33287.220370305b44c833f1; '
               'ecLm_2132_seccodecSbxLr4Z=33292.431347698174de7136; ecLm_2132_noticeTitle=1; '
               'ecLm_2132_seccodecSIm5ID8=17330.e541a1b07881b6f209; ecLm_2132_ignore_notice=1; '
               'ecLm_2132_seccodecSFb5I75=17370.c6234b9b674f0f37b9; '
               'ecLm_2132_seccodecSYS7b7W=17401.79a26ddb45ea11c1e5; ecLm_2132_sendmail=1; ecLm_2132_checkpm=1 '
}
dirname='./北京小姐姐大全/'
os.mkdir(dirname)

url='http://www.52bjxjj.me/forum.php?mod=viewthread&tid=1'

seccess=0
#########获取文本内容-格式化文本内容###############
def gettext(res):

    xx = 'title:' + soup.title.string.split('-')[0].replace(' ', '') + '\n\n'+doc('.t_f').text()  # 获取title标题
    a2 = xx.replace('：\n', ':').replace(':\n', ':')
    a3 = re.sub(r'暗(\s+)号', '暗号', a2)
    a4 = a3.replace('52bjxjj', '帅帅\n\n车友评论：').strip()



    return a4
##########获取文本内容-格式化文本内容##############


#########创建不同目录-分别以title命名#############
def mkdirdir(dir, str1, imagename, bpic):
    os.mkdir(dirname + dir)
    dirs = dirname + dir + '/' + dir + '.txt'
    file = open(dirs, 'a+', encoding='utf-8')
    file.write(str1)
    file.close()
    num = len(imagename)
    if num:
        for i in range(num):
            with open(dirname+dir+'/'+imagename[i-1], mode='wb') as pic:
                pic.write(bpic[i-1])
                newjpg = Image.open(dirname+dir+'/'+imagename[i-1])
                newjpg.save(dirname+dir+'/'+imagename[i-1])

#########创建不同目录-分别以title命名#############


###################爬取图片####################
def getpic():
    pic = doc('.zoom')
    url = 'http://www.52bjxjj.me/'
    piclist=[]
    imagename=[]
    for picurl in pic:
        picu = picurl.get('file')
        piclist.append(url+picu)
        imagename.append(picu.split('/')[-1])
    return imagename, piclist
###################爬取图片####################



###程序主入口###
if __name__=='__main__':
    for i in range(1,1021):
        try:
            url = 'http://www.52bjxjj.me/forum.php?mod=viewthread&tid={}'.format(i)
            ss = requests.Session()
            res = ss.get(url, headers=headers, timeout=3)                      #遍历获取每一个url实例对象
            if res.status_code==200:
                soup = BeautifulSoup(res.text, 'lxml')
                dir = soup.title.string.split('-')[0].replace(' ', '')
                doc = pq(res.text)
                str1 = gettext(res)
                imagename, piclist = getpic()
                bpic=[]
                for picurl in piclist:
                    pic2 = ss.get(picurl, timeout=3)
                    bpic.append(pic2.content)
                mkdirdir(dir, str1, imagename, bpic)
                seccess += 1
                print('已成功爬取{}条数据~！'.format(seccess))
                res.close()
            else:
                print('[-]抱歉，指定的主题不存在或已被删除或正在被审核---id为{}无数据'.format(i))
        except:
            continue










