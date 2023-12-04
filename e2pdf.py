import tkinter
import requests
import ctypes
import re
import time
import os
import tkinter.messagebox
from PIL import Image
import threading
from img2pdf import pdfconvert

def threadit(func, *args):
    t = threading.Thread(target=func, args=args)
    t.start()

def start():
    startimg = Image.open("rip,CE.png")
    startimg.show()
    startimg.close()
    startimg2 = Image.open("pic.png")
    startimg2.show()
    print("化学已死，计算机当立")

threadit(start)

def validateTitle(title):  # 替换非法字符
    rstr = r"[\:\*\?\|]"
    rstr2 = r"[\"]"
    rstr3 = r"[\<\>]"
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    new_title = re.sub(rstr2, "'", new_title)  # 替换单引号
    new_title = re.sub(rstr3, "[]", new_title)  # 替换为方括号
    return new_title

headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' } #伪装成浏览器
proxies = {
    "http": "127.0.0.1:7890",
    "https": "127.0.0.1:7890",
}

try:
    proxies["http"] = open("proxy.ini", "r").readline()
    proxies["https"] = open("proxy.ini", "r").readline()    #读取代理文件
except:
    print("未找到代理文件，使用默认代理...")

folder = os.path.exists("Downloads")
if not folder:
    os.makedirs("Downloads")
    print("已创建文件夹Downloads")
folder = os.path.exists("PDFs")
if not folder:
    os.makedirs("PDFs")
    print("已创建文件夹PDFs") #创建文件夹

ctypes.windll.shcore.SetProcessDpiAwareness(1) # 适配高分屏

dlist = []

class gallery:
    link = ""
    title = ""
    pages = 0
    firstpage = ""
    def __init__(self, link, title, pages,firstpage):
        self.link = link
        self.title = title
        self.pages = pages
        self.firstpage = firstpage

class ipg:
    link = ""
    def __init__(self, link):
        self.link = link #我忘了为什么要这么写，写了有什么用，但是删了可能会报错

def download1(link,count,i): #下载一个画廊里的所有图片
    try:
        r = requests.get(link, proxies=proxies, headers=headers)
        log = "第{}本漫画,正在解析第{}张图片".format(i,count)
    except:
        print("页面文件获取失败，重试中")
        try:
            r = requests.get(link, proxies=proxies, headers=headers)
            log = "第{}本漫画,正在解析第{}张图片".format(i,count)
        except:
            print("重试失败")
            raise Exception("无法连接到E站")
    print(log)

    try:
        imglink = str(re.findall(r'<img id="img" src="([\s\S]*?)" style', r.text)[0])
    except:
        raise Exception("图片链接解析失败，可能是链接错误或者E站已经改版")
    
    try:
        nextlink = str(re.search(r'<a id="next"[^>]+href="([^"]*?)"', r.text).group(1))
    except:
        raise Exception("下一页链接解析失败，可能是链接错误或者E站已经改版")

    with open("Downloads/{}/{:0>6d}.jpg".format(dlist[i-1].title,count), "wb") as code:
        try:
            code.write(requests.get(imglink, proxies=proxies, headers=headers).content)
            log = "第{}本漫画，第{}张图片下载完成".format(i,count)
        except:
            print("下载失败，重试中")
            try:
                code.write(requests.get(imglink, proxies=proxies, headers=headers).content)
                log = "第{}本漫画，第{}张图片下载完成".format(i,count)
            except:
                print("重试失败")
                raise Exception("无法连接到E站")
        print(log)
    return nextlink

MainActivity = tkinter.Tk()
MainActivity.title("E站漫画下载器")
MainActivity.geometry("900x800")
title = tkinter.Label(MainActivity, text="E站漫画下载器",font=("微软雅黑", 20))
title.grid(row=0,column=0)
entry = tkinter.Entry(MainActivity, font=("微软雅黑", 15))
entry.grid(row=1,column=0)
listbox = tkinter.Listbox(MainActivity, font=("微软雅黑", 15))
listbox.grid(row=2,column=0)

def addtolist(): #加入下载列表
    try :
        flatg = requests.get(entry.get(), proxies=proxies, headers=headers)
    except:
        raise Exception("无法连接到E站")
    try:
        gtitle = validateTitle(str(re.findall(r'<h1 id="gn">([\s\S]*?)</h1>', flatg.text)[0]))
        tpages = int(re.findall(r'Length:</td><td class="gdt2">([\s\S]*?) pages', flatg.text)[0])
        firstpage = str(re.findall(r'no-repeat"><a href="([\s\S]*?)"><img alt=', flatg.text)[0])
    except:
        raise Exception("解析失败，可能是链接错误或者E站已经改版")
    for downloaded in next(os.walk("Downloads"))[1]:
        if gtitle == downloaded:
            tkinter.messagebox.showinfo("提示", "该漫画已经在下载列表中")
            return 0
    listbox.insert("end", gtitle)
    dlist.append(gallery(entry.get(), gtitle, tpages, firstpage))
    entry.delete(0,"end")

addbutton = tkinter.Button(MainActivity, text="加入列表",font=("微软雅黑", 15),command=addtolist)
addbutton.grid(row=1,column=2)
def download(): #处理下载列表
    global dlist
    icont = 0
    for i in dlist:
        icont += 1
        os.mkdir("Downloads/{}".format(i.title))
        nextilink = download1(i.firstpage,1,icont)
        for j in range(2,i.pages+1):
            try:
                nextilink = download1(nextilink,j,icont)
                time.sleep(0.5)
            except:
                raise Exception("无法连接到E站")
        pdfconvert("Downloads/{}".format(i.title),"PDFs/{}.pdf".format(i.title))
    dlist = []
    listbox.delete(0,"end")
startbutton = tkinter.Button(MainActivity, text="开始下载",font=("微软雅黑", 15),command=lambda:threadit(download))
startbutton.grid(row=1,column=3)
time.sleep(1) #等待启动图加载
MainActivity.mainloop()