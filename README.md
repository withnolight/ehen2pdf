# 一个基于python语言的E-hentai漫画下载及PDF生成器
## 使用之前
### 网络配置

此软件必须使用代理。  
可在proxy.ini文件中指定自定义proxy。⚠️此功能未经测试，出现问题时请改变proxy为默认⚠️  
默认proxy为`127.0.0.1:7890`  
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
可在控制台查看进度。
## 克服的困难（我为什么有自信提交此项目）
![化工已死]（rip,CE.png）
1. 大战正则，和文心一言比赛谁正则写得好，最后双双败给Github Copilot（悲  
2. 大战tk，写出了大气磅礴的GUI（迫真  
3. 大战多线程，成功避免了GUI假死，顺带解决了启动图加载过慢阻塞了GUI的问题（喜  
4. 大战Windows非法路径名（很难排查，很好解决）  
5. 大战文本缩放比例，高分屏也能正确显示（有基础知识，不难）  