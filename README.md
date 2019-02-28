# ConfConvertor
旨在能够使用一套配置通过转换API转换成适应于各类科学上网的配置文件

# 已经完成的功能
将Surge3Pro转换成不带有RULE-SET,Policy-Path的普通形式

# 使用方法
## 方法一
如果担心数据安全性等问题，可以选择在自己的服务器上搭建，源代码已经在代码库中给出
## 方法二
我将该脚本部署在了自己的GCP上。
URL:https://asia-northeast1-trans-filament-233005.cloudfunctions.net/Surge3Expand
支持的参数：url(必须）

url:将Surge3的配置文件从url下载下来，将RULE-SET，Policy-Path进行展开，返回转换后的文件。
