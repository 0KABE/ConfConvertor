# 使用Filter中的rename参数来自定义节点信息
## 原理
>正则表达式（英语：Regular Expression，在代码中常简写为regex、regexp或RE），又称正规表示式、正规表示法、正规运算式、规则运算式、常规表示法，是计算机科学的一个概念。正则表达式使用单个字符串来描述、匹配一系列符合某个句法规则的字符串。在很多文本编辑器里，正则表达式通常被用来检索、替换那些符合某个模式的文本。--https://zh.wikipedia.org/wiki/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F  

简单来说，正则表达式能够用于表达相似字符串的集合，例如Surge的节点list中每一行都是相同的格式，因此我们能够使用正则表达式来处理它，甚至是对每一行的内容做出相同的更改。  

为了能够对每一行的内容做出更改，我们需要在正则表达式中对每一个组起一个别名，我们在每个圆括号()中添加?P<别名>来对这个圆括号内的内容添加一个别名  

对于下面的正则表达式：
```
(?P<Domestic>.*?) *-> *(?P<Area>.*?) *(?P<No>\d*) *\| *(?P<ISP>IPLC?)(?P<Remain>.*=.*)
```
依次对每个括号内匹配到的内容起了别名：Demestic, Area, No, ISP, Remain  

**需要注意的是，正则表达式将会对一行的所有数据进行匹配，因此，需要一个别名来代表一行中剩余的字符串内容，否则对于上面的正则，将会舍弃每一行IPLC后所有的内容，上方的正则中Remain别名的作用便是这个。**  

**以上对于接下来如果对list中每一行的内容自定义很重要，请务必理解。**  

添加完别名后，就可以使用rename参数来对每一行的内容自定义了  
对于这个rename参数：
```
Domestic
 _ 
Area
 + 
ISP
 
No
Remain
```
API将会从上到下取出Domestic Area ISP No Remain中匹配到的内容，重新拼接成一个新的字符串。  
**API将一行当作一个别名，如果遇到的不是在正则中定义的别名，则会直接附加在新字符串中** 

## 注意事项
* 不要忘记对参数url encode
* 不要忘记匹配每一行的剩余内容，否则API将会直接舍弃

## 示例
本例将简单介绍如何对该list过滤节点的同时对节点自定义  
如果你完全理解本脚本的运作方式，你会明白他能做的不仅仅是自定义节点名称，甚至能够更改每条中特定部分的字段，例如更改以下obfs-host的值，删除udp-replay=true等等  
**以下是范例中使用的原始待自定义的list:**  
```
🇨🇳 中国上海 - Back = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇨🇳 中国上海 -> 台湾 1 | BGP = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇺🇸 中国上海 -> 美国 2 | BGP = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇯🇵 中国上海 -> 日本 3 | BGP = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇯🇵 中国上海 -> 日本 1 | IPLC = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇯🇵 中国上海 -> 日本 2 | IPLC = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇯🇵 中国上海 -> 日本 3 | IPLC = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇯🇵 中国上海 -> 日本 4 | IPLC = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇯🇵 中国上海 -> 日本 5 | IPLC = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇺🇸 中国上海 -> 美国 1 | IPLC = ss, xxx.xxx.xxx.xxx, 152, encrypt-method=chacha20-ietf-poly1305, password=UrTAdN, obfs=tls, obfs-host=8d9c317407.wns.windows.com, udp-relay=true
🇷🇺 中国北京 -> 俄罗斯 1 | BGP = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇩🇪 中国北京 -> 德国 2 | BGP = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇩🇪 中国北京 -> 德国 3 | BGP = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇨🇳 中国徐州 - Back = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇭🇰 中国杭州 -> 香港 1 | BGP = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇭🇰 中国深圳 -> 香港 1 | BGP = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇭🇰 中国深圳 -> 香港 2 | BGP = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇭🇰 中国深圳 -> 香港 3 | BGP = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇲🇴 中国深圳 -> 澳门 4 | BGP = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇸🇬 中国深圳 -> 新加坡 1 | IPLC = ss, xxx.xxx.xxx.xxx, 152, encrypt-method=chacha20-ietf-poly1305, password=UrTAdN, obfs=tls, obfs-host=8d9c317407.wns.windows.com, udp-relay=true
🇭🇰 中国深圳 -> 香港 1 | IPLC = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇭🇰 中国深圳 -> 香港 2 | IPLC = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇭🇰 中国深圳 -> 香港 3 | IPLC = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇭🇰 中国深圳 -> 香港 4 | IPLC = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇭🇰 中国深圳 -> 香港 5 | IPLC = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇭🇰 中国深圳 -> 香港 6 | IPLC = ss, xxx.xxx.xxx.xxx, 152, encrypt-method=chacha20-ietf-poly1305, password=UrTAdN, obfs=tls, obfs-host=8d9c317407.wns.windows.com, udp-relay=true
🇨🇳 中国镇江 - Back = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
```

API Filter的参数  
url encode前  
```
regex=(?P<Domestic>.*?) *-> *(?P<Area>.*?) *(?P<No>\d*) *\| *(?P<ISP>IPLC?)(?P<Remain>.*=.*)
rename=Domestic
 _ 
Area
 + 
ISP
 
No
Remain
```
url encode后  
```
regex=%28%3FP%3CDomestic%3E.%2A%3F%29%20%2A-%3E%20%2A%28%3FP%3CArea%3E.%2A%3F%29%20%2A%28%3FP%3CNo%3E%5Cd%2A%29%20%2A%5C%7C%20%2A%28%3FP%3CISP%3EIPLC%3F%29%28%3FP%3CRemain%3E.%2A%3D.%2A%29
rename=Domestic%0A%20_%20%0AArea%0A%20%2B%20%0AISP%0A%20%0ANo%0ARemain
```

返回的内容
```
🇯🇵 中国上海 _ 日本 + IPLC 1 = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇯🇵 中国上海 _ 日本 + IPLC 2 = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇯🇵 中国上海 _ 日本 + IPLC 3 = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇯🇵 中国上海 _ 日本 + IPLC 4 = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇯🇵 中国上海 _ 日本 + IPLC 5 = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇺🇸 中国上海 _ 美国 + IPLC 1 = ss, xxx.xxx.xxx.xxx, 152, encrypt-method=chacha20-ietf-poly1305, password=UrTAdN, obfs=tls, obfs-host=8d9c317407.wns.windows.com, udp-relay=true
🇸🇬 中国深圳 _ 新加坡 + IPLC 1 = ss, xxx.xxx.xxx.xxx, 152, encrypt-method=chacha20-ietf-poly1305, password=UrTAdN, obfs=tls, obfs-host=8d9c317407.wns.windows.com, udp-relay=true
🇭🇰 中国深圳 _ 香港 + IPLC 1 = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇭🇰 中国深圳 _ 香港 + IPLC 2 = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇭🇰 中国深圳 _ 香港 + IPLC 3 = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇭🇰 中国深圳 _ 香港 + IPLC 4 = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇭🇰 中国深圳 _ 香港 + IPLC 5 = ss, xxx.xxx.xxx.xxx, 37883, encrypt-method=xchacha20-ietf-poly1305, password=xxxxxxxxx, obfs=tls, obfs-host=download.windowsupdate.com, udp-relay=true
🇭🇰 中国深圳 _ 香港 + IPLC 6 = ss, xxx.xxx.xxx.xxx, 152, encrypt-method=chacha20-ietf-poly1305, password=UrTAdN, obfs=tls, obfs-host=8d9c317407.wns.windows.com, udp-relay=true
```