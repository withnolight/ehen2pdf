import tkinter
import requests
import ctypes
import re
import time
import os
from PIL import Image

headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' }
proxies = {
    "http": "127.0.0.1:7890",
    "https": "127.0.0.1:7890",
}

try:
    proxies["http"] = open("proxies.ini", "r").readline()
    proxies["https"] = open("proxies.ini", "r").readline()
except:
    print("未找到代理文件，使用默认代理")

print('我们仍然一无所知。')

def rea(path, pdf_name):
    file_list = os.listdir(path)
    pic_name = []
    im_list = []
    for x in file_list:
        if "jpg" in x or 'png' in x or 'jpeg' in x:
            pic_name.append(x)
 
    pic_name.sort()
    new_pic = []
 
    for x in pic_name:
        if "jpg" in x:
            new_pic.append(x)
 
    for x in pic_name:
        if "png" in x:
            new_pic.append(x)
 
    print("hec", new_pic)
 
    im1 = Image.open(os.path.join(path, new_pic[0]))
    new_pic.pop(0)
    for i in new_pic:
        img = Image.open(os.path.join(path, i))
        # im_list.append(Image.open(i))
        if img.mode == "RGBA":
            img = img.convert('RGB')
            im_list.append(img)
        else:
            im_list.append(img)
    im1.save(pdf_name, "PDF", resolution=100.0, save_all=True, append_images=im_list)
    print("输出文件名称：", pdf_name)

folder = os.path.exists("Downloads")
if not folder:
    os.makedirs("Downloads")
    print("已创建文件夹Downloads")
folder = os.path.exists("PDFs")
if not folder:
    os.makedirs("PDFs")
    print("已创建文件夹PDFs")
ctypes.windll.shcore.SetProcessDpiAwareness(1)

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
        self.link = link

def download1(link,count,i):
    r = requests.get(link, proxies=proxies, headers=headers)
    log = "第{}本漫画,正在解析第{}张图片".format(i,count)
    print(log)
    imglink = str(re.findall(r'<img id="img" src="([\s\S]*?)" style', r.text)[0])
    print(log)
    nextlink = str(re.search(r'<a id="next"[^>]+href="([^"]*?)"', r.text).group(1))
    print(nextlink)
    print(imglink)
    print(log)
    with open("Downloads/{}/{:0>6d}.jpg".format(dlist[i-1].title,count), "wb") as code:
        code.write(requests.get(imglink, proxies=proxies, headers=headers).content)
        log = "第{}本漫画，第{}张图片下载完成".format(i,count)
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
def addtolist():
    try :
        flatg = requests.get(entry.get(), proxies=proxies, headers=headers)
        gtitle = str(re.findall(r'<h1 id="gn">([\s\S]*?)</h1>', flatg.text)[0])
        tpages = int(re.findall(r'Length:</td><td class="gdt2">([\s\S]*?) pages', flatg.text)[0])
        firstpage = str(re.findall(r'no-repeat"><a href="([\s\S]*?)"><img alt=', flatg.text)[0])
        listbox.insert("end", gtitle)
        dlist.append(gallery(entry.get(), gtitle, tpages, firstpage))
    except:
        raise Exception("无法连接到E站")
addbutton = tkinter.Button(MainActivity, text="加入列表",font=("微软雅黑", 15),command=addtolist)
addbutton.grid(row=1,column=2)
def download():
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
        rea("Downloads/{}".format(i.title),"PDFs/{}.pdf".format(i.title))
startbutton = tkinter.Button(MainActivity, text="开始下载",font=("微软雅黑", 15),command=download)
startbutton.grid(row=1,column=3)
MainActivity.mainloop()