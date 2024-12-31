# my_vlc
一款基于vlc、python的数字键盘可控制的iptv流播放程序


## 使用方法
下载两个源代码文件，并安装依赖，使用pyinstaller -f my_vlc.py进行打包。
将exe文件，已经整理好的m3u文件放置到vlc压缩包版解压后的文件夹内，双击exe执行文件即可。
如图：
![image](https://github.com/user-attachments/assets/de3d8ea8-0860-41d1-97f1-f7f38b9ec271)



## 使用的技术
开源的vlc播放器，需要下载压缩包版本；
python3.10以及第三方库，详见源码仓库。



## 其他信息
m3u文件的内容格式如下：
```
#EXTM3U\
#EXTINF:-1,CCTV-1
http://192.168.2.1:4022/rtp/239.254.200.45:8008

#EXTINF:-1,CCTV-2
http://192.168.2.1:4022/rtp/239.254.200.158:6000

#EXTINF:-1,CCTV-3高清
http://192.168.2.1:4022/rtp/239.254.201.152:7205

#EXTINF:-1,CCTV-4
http://192.168.2.1:4022/rtp/239.254.200.190:6307

```
