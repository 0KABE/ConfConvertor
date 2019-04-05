# ConfConvertor
旨在能够使用一套配置通过转换API转换成适应于各类科学上网的配置文件

## 停止维护：  
因为结构混乱，增加新功能困难，且时间复杂度过高，已经停止维护  
将Surge3Pro转换成不带有RULE-SET,Policy-Path的普通形式  
直接将Surge3Pro转换成ClashForWindows支持的配置形式  
停止维护的API：  
Surge3Expand  
Surge3ToClash


## 正在维护：
拟通过在类Surge3Pro的配置文件上增加一些Clash的特殊的内容。
例如：  
当调用导出为Surge配置文件时，从类Surge3Pro的配置文件中抽取Surge3Pro支持的内容（例如Surge 不支持V2ray），组成Surge3Pro的配置文件

可以实现一份配置文件同时支持Clash & Surge3

## API: Surge3介绍：  
相比与Surge3Expand 新的API Surge3不在默认将policy-path, RULE-SET 全部展开  

在Surge3Pro中，不支持policy-path与其他policy-path混用或policy-path与其他策略组混用  
即如果需要使用policy-path来远程下载节点信息，则该策略组将只允许一个policy-path  
例如：  
policy1 = select, policy-path=www.example.com/path/file.list  合法  
policy2 = select, policy-path=www.example.com/path/file.list, policy1  非法  
policy3 = select, policy-path=www.example.com/path/file1.list, policy-path=www.example.com/path/file2.list  非法  

现在，API Surge3将会判断策略组中是否存在上述的情况，若存在上述的在Surge中非法的情况，才会对所有policy-path进行展开  
如果策略组中没有存在上述的情况，保留policy-path交给Surge3展开总是更好的


**如果担心数据安全性等问题，可以选择在自己的服务器上搭建，源代码已经在代码库中给出**  
**如果遇到BUG 或者 有好的Feature 欢迎提Issue**

# 使用方法
## Surge3Expand
URL:https://asia-northeast1-trans-filament-233005.cloudfunctions.net/Surge3Expand  
支持的参数：url(必须）

url:将Surge3的配置文件从url下载下来，将RULE-SET，Policy-Path进行展开，返回转换后的文件。

## Surge3ToClash
URL:https://asia-northeast1-trans-filament-233005.cloudfunctions.net/Surge3ToClash  
支持的参数：url(必须）

url:将Surge3的配置文件从url下载下来，将RULE-SET，Policy-Path进行展开，转换成Clash支持的文件。

## Surge3
URL:https://asia-east2-trans-filament-233005.cloudfunctions.net/surge3  
支持的参数：url(必须），filename（非必须），interval（非必须），strict（非必须）

url: 待转换的类Surge3Pro配置url地址  
filename：返回的配置文件名称（默认返回Config.conf）  
interval：托管配置的更新间隔（默认86400s）  
strict：（true/false）  在更新间隔到达时是否强制更新，如果为false则在更新失败后依旧使用原来的托管配置