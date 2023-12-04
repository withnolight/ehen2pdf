# 一个基于python语言的E-hentai漫画下载及PDF生成器
## 使用之前
### 网络配置

此软件必须使用代理。  
可在proxy.ini文件中指定自定义proxy。默认proxy为`127.0.0.1:7890`  
即使你所在的网络能直连E-hentai，这也是必须的。这种情况可以设置代理模式为Direct.  
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
2.下载过程中GUI假死