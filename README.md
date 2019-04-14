# ConfConvertor
旨在能够使用一套配置通过转换API转换成适应于各类科学上网的配置文件

## 停止维护：  
因为结构混乱，增加新功能困难，且时间复杂度过高，已经停止维护  
将Surge3Pro转换成不带有RULE-SET,Policy-Path的普通形式  
直接将Surge3Pro转换成ClashForWindows支持的配置形式  
停止维护的API：  
* Surge3Expand  
* Surge3ToClash



## 正在维护：
拟通过在类Surge3Pro的配置文件上增加一些Clash的特殊的内容。
例如：  
当调用导出为Surge配置文件时，从类Surge3Pro的配置文件中抽取Surge3Pro支持的内容（例如Surge 不支持V2ray），组成Surge3Pro的配置文件

可以实现一份配置文件同时支持Clash & Surge3

## API: Surge3介绍：  
相比与Surge3Expand 新的API Surge3不在默认将policy-path, RULE-SET 全部展开  
**去除load-balance**  

在Surge3Pro中，不支持policy-path与其他policy-path混用或policy-path与其他策略组混用  
即如果需要使用policy-path来远程下载节点信息，则该策略组将只允许一个policy-path  
例如：  
```
policy1 = select, policy-path=www.example.com/path/file.list  合法  
policy2 = select, policy-path=www.example.com/path/file.list, policy1  非法  
policy3 = select, policy-path=www.example.com/path/file1.list, policy-path=www.example.com/path/file2.list  非法  
```
~~现在，API Surge3将会判断策略组中是否存在上述的情况，若存在上述的在Surge中非法的情况，才会对所有policy-path进行展开  
如果策略组中没有存在上述的情况，保留policy-path交给Surge3展开总是更好的~~  
**因为Surge3托管文件不能手动更新PolicyPath  
现在API Surge3 将会直接将policypath展开**

## API: Clash介绍：  
**支持load-balance**  
在Clash中，靠后的策略组中包含的策略组必须位于该策略组前面，而Surge中则没有这个限制，可以任意排序。  
在这个API中，Clash将会通过排序来使得策略组的顺序满足Clash的要求。
例如：  
```
- name: Policy1
  type: select
  proxies:
  - Policy2
  - Policy3
- name: Policy2
  type: select
  proxies:
  - Node1
  - Node2
- name: Policy3
  type: select
  proxies:
  - Node3
  - Node4
```
上述的序列关系无法在Clash使用，需要对该策略组的顺序重新排列
```
- name: Policy2
  type: select
  proxies:
  - Node1
  - Node2
- name: Policy3
  type: select
  proxies:
  - Node3
  - Node4
- name: Policy1
  type: select
  proxies:
  - Policy2
  - Policy3
```
以上便是一个排列后在Clash中合法的顺序组合  
除此之外，该API将会对policy-path以及RULE-SET进行展开，去除某些在clash中不支持的内容。  
例如：  
* reject-tinygif
* USER-AGENT
* MITM
* 等等




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

## Clash
URL:https://asia-east2-trans-filament-233005.cloudfunctions.net/clash  
参数：url（必须），filename（非必须），snippet（非必须）  

url: 待转换的类Surge3Pro配置url地址  
filename：返回的配置文件名称（默认返回Config.yml）  
snippet：为clash配置附加额外的参数（例如DNS）参数格式为yaml格式（同Clash）  

# 使用方法(demo):  
因为API需要一个url参数来获取类Surge配置文件，因此一种方法是使用GitHub私有gist来远程存放链接  
例如， 现在的远程链接： https://gist.githubusercontent.com/0KABE/1f448c7b26db7a3c5830a40f33021e8f/raw/DEMO.conf  
则：  
在Surge3Pro中的托管链接为：https://asia-east2-trans-filament-233005.cloudfunctions.net/surge3?url=https://gist.githubusercontent.com/0KABE/1f448c7b26db7a3c5830a40f33021e8f/raw/DEMO.conf  
在Clash中的托管链接为：https://asia-east2-trans-filament-233005.cloudfunctions.net/clash?https://gist.githubusercontent.com/0KABE/1f448c7b26db7a3c5830a40f33021e8f/raw/DEMO.conf

# 感谢:  
* Shiro  

# 打赏:  
```
#吱口令#长按复制此条消息，打开支付宝给我转账ijL3kr36HM
```
# Telegram：  
https://t.me/Rin_OKAB3