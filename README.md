# 一个基于python语言的E-hentai漫画下载及PDF生成器
## 使用之前
### 网络配置

**无论何时，此软件必须使用本地代理，端口号为7890。**即使你所在的网络能直连E-hentai，这也是必须的。这种情况可以设置代理模式为Direct.  
推荐使用Clash。
网络的不稳定会导致程序崩溃。
### 环境配置
在python 3.10 版本测试。  
要安装依赖，`pip install -r requirements.txt`.
## 使用时
在终端输入`python .\e2pdf.py`(Powershell) 或`python e2pdf.py`(CMD)
在文本框内输入正确E-hentai画廊链接。例如<https://e-hentai.org/g/2750100/2a4420be03>。  
在加入足够的链接后，即可开始。  
过程中GUI界面未响应完全正常，可在控制台查看进度。
## 已知bug
1.反复下载同一个画廊导致程序崩溃
2.下载过程中GUI假死