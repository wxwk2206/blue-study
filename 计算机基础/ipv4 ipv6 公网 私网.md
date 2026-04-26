### <font style="color:rgb(15, 17, 21);">1. IPv4</font>
**<font style="color:rgb(15, 17, 21);">核心解释</font>**<font style="color:rgb(15, 17, 21);">：IPv4是</font>**<font style="color:rgb(15, 17, 21);">第四版互联网协议</font>**<font style="color:rgb(15, 17, 21);">，是当前互联网最主要、最广泛使用的“地址系统”和“通信规则”。它定义了数据包如何在网络中传输，以及设备如何被寻址。</font>

**<font style="color:rgb(15, 17, 21);">关键特点</font>**<font style="color:rgb(15, 17, 21);">：</font>

+ **<font style="color:rgb(15, 17, 21);">地址格式</font>**<font style="color:rgb(15, 17, 21);">：由4个用点分隔的十进制数组成，每个数范围是0-255。例如：</font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">192.168.1.1</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">或</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">8.8.8.8</font>`<font style="color:rgb(15, 17, 21);">（Google的DNS服务器）。</font>
+ **<font style="color:rgb(15, 17, 21);">地址长度</font>**<font style="color:rgb(15, 17, 21);">：总共32位（二进制），因此它提供的地址总数是有限的，约为</font><font style="color:rgb(15, 17, 21);"> </font>**<font style="color:rgb(15, 17, 21);">43亿个</font>**<font style="color:rgb(15, 17, 21);">。</font>
+ **<font style="color:rgb(15, 17, 21);">地址耗尽</font>**<font style="color:rgb(15, 17, 21);">：由于互联网爆炸式增长，43亿个地址早已不够用，这就是催生IPv6和NAT技术（后面会讲）的主要原因。</font>

**<font style="color:rgb(15, 17, 21);">简单比喻</font>**<font style="color:rgb(15, 17, 21);">：IPv4就像是</font>**<font style="color:rgb(15, 17, 21);">传统的电话号码系统</font>**<font style="color:rgb(15, 17, 21);">（比如7位或8位号码）。这个系统很好用，但号码资源有限，随着用户增多，号码就不够分配了。</font>

---

### <font style="color:rgb(15, 17, 21);">2. IPv6</font>
**<font style="color:rgb(15, 17, 21);">核心解释</font>**<font style="color:rgb(15, 17, 21);">：IPv6是</font>**<font style="color:rgb(15, 17, 21);">第六版互联网协议</font>**<font style="color:rgb(15, 17, 21);">，是旨在解决IPv4地址耗尽问题的“下一代”地址系统和通信规则。</font>

**<font style="color:rgb(15, 17, 21);">关键特点</font>**<font style="color:rgb(15, 17, 21);">：</font>

+ **<font style="color:rgb(15, 17, 21);">地址格式</font>**<font style="color:rgb(15, 17, 21);">：由8组4位的十六进制数组成，组之间用冒号分隔。例如：</font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">2001:0db8:85a3:0000:0000:8a2e:0370:7334</font>`<font style="color:rgb(15, 17, 21);">。为了简化，前面的0可以省略，连续的0可以压缩为</font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">::</font>`<font style="color:rgb(15, 17, 21);">。</font>
+ **<font style="color:rgb(15, 17, 21);">地址长度</font>**<font style="color:rgb(15, 17, 21);">：总共128位（二进制），提供的地址数量是一个天文数字（约3.4 x 10³⁸ 个）。形象地说，</font>**<font style="color:rgb(15, 17, 21);">地球上的每一粒沙子都可以分配一个IP地址</font>**<font style="color:rgb(15, 17, 21);">。</font>
+ **<font style="color:rgb(15, 17, 21);">优势</font>**<font style="color:rgb(15, 17, 21);">：</font>
    - **<font style="color:rgb(15, 17, 21);">近乎无限的地址</font>**<font style="color:rgb(15, 17, 21);">：从根本上解决了地址枯竭问题。</font>
    - **<font style="color:rgb(15, 17, 21);">更高效</font>**<font style="color:rgb(15, 17, 21);">：数据包处理效率更高，无需像IPv4那样进行复杂的碎片化处理。</font>
    - **<font style="color:rgb(15, 17, 21);">更安全</font>**<font style="color:rgb(15, 17, 21);">：IPsec（网络层安全协议）是其原生组成部分。</font>
    - **<font style="color:rgb(15, 17, 21);">即插即用</font>**<font style="color:rgb(15, 17, 21);">：设备可以更容易地为自己配置地址。</font>

**<font style="color:rgb(15, 17, 21);">简单比喻</font>**<font style="color:rgb(15, 17, 21);">：IPv6就像是</font>**<font style="color:rgb(15, 17, 21);">升级后的电话号码系统</font>**<font style="color:rgb(15, 17, 21);">，号码位数变得极长（比如几十位），确保了未来几百年内都有足够的号码可以分配，永无枯竭之忧。</font>

---

### <font style="color:rgb(15, 17, 21);">3. 公网IP</font>
**<font style="color:rgb(15, 17, 21);">核心解释</font>**<font style="color:rgb(15, 17, 21);">：公网IP地址是</font>**<font style="color:rgb(15, 17, 21);">在全局互联网上唯一、可被直接路由的地址</font>**<font style="color:rgb(15, 17, 21);">。它就像你家的</font>**<font style="color:rgb(15, 17, 21);">全球唯一邮寄地址</font>**<font style="color:rgb(15, 17, 21);">。</font>

**<font style="color:rgb(15, 17, 21);">关键特点</font>**<font style="color:rgb(15, 17, 21);">：</font>

+ **<font style="color:rgb(15, 17, 21);">全球唯一性</font>**<font style="color:rgb(15, 17, 21);">：在整个互联网上，任何一个公网IP地址都只属于一个设备（或一个网络出口）。</font>
+ **<font style="color:rgb(15, 17, 21);">可直接访问</font>**<font style="color:rgb(15, 17, 21);">：任何连接到互联网的设备，理论上都可以通过这个地址找到你。</font>
+ **<font style="color:rgb(15, 17, 21);">由ISP分配</font>**<font style="color:rgb(15, 17, 21);">：通常由你的互联网服务提供商（如电信、联通）分配给你。它可能是固定的（专线），也可能是动态的（家庭宽带每次拨号可能会变）。</font>
+ **<font style="color:rgb(15, 17, 21);">稀缺资源</font>**<font style="color:rgb(15, 17, 21);">：由于IPv4地址耗尽，一个家庭或公司通常只被分配</font>**<font style="color:rgb(15, 17, 21);">一个</font>**<font style="color:rgb(15, 17, 21);">IPv4公网地址。</font>

**<font style="color:rgb(15, 17, 21);">作用</font>**<font style="color:rgb(15, 17, 21);">：当你访问百度、谷歌时，你的请求就是通过你的</font>**<font style="color:rgb(15, 17, 21);">公网IP</font>**<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">发出去，然后对方的服务器再通过这个</font>**<font style="color:rgb(15, 17, 21);">公网IP</font>**<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">将数据返回给你。它是你在互联网上的“身份证”。</font>

---

### <font style="color:rgb(15, 17, 21);">4. 私网IP</font>
**<font style="color:rgb(15, 17, 21);">核心解释</font>**<font style="color:rgb(15, 17, 21);">：私网IP地址是</font>**<font style="color:rgb(15, 17, 21);">在私有网络（如家庭、公司内部局域网）内部使用的地址</font>**<font style="color:rgb(15, 17, 21);">，</font>**<font style="color:rgb(15, 17, 21);">不能在公网上被直接路由</font>**<font style="color:rgb(15, 17, 21);">。它就像你公司内部的分机号，或者你家小区里的门牌号。</font>

**<font style="color:rgb(15, 17, 21);">关键特点</font>**<font style="color:rgb(15, 17, 21);">：</font>

+ **<font style="color:rgb(15, 17, 21);">本地唯一性</font>**<font style="color:rgb(15, 17, 21);">：只在你的私有网络内部是唯一的。</font>
+ **<font style="color:rgb(15, 17, 21);">不可公网路由</font>**<font style="color:rgb(15, 17, 21);">：如果直接用私网IP去访问互联网，数据包会被丢弃，因为互联网路由器不认识这些地址。</font>
+ **<font style="color:rgb(15, 17, 21);">可重复使用</font>**<font style="color:rgb(15, 17, 21);">：不同家庭的局域网可以使用相同的私网IP段（比如大家都用</font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">192.168.1.x</font>`<font style="color:rgb(15, 17, 21);">），这大大节省了公网IP地址。</font>
+ **<font style="color:rgb(15, 17, 21);">保留地址段</font>**<font style="color:rgb(15, 17, 21);">：IPv4协议专门保留了以下几段地址作为私网IP：</font>
    - `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">10.0.0.0</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">-</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">10.255.255.255</font>`
    - `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">172.16.0.0</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">-</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">172.31.255.255</font>`
    - `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">192.168.0.0</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">-</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">192.168.255.255</font>`

**<font style="color:rgb(15, 17, 21);">作用</font>**<font style="color:rgb(15, 17, 21);">：你家里的电脑、手机、智能电视等设备，获取的都是路由器分配的</font>**<font style="color:rgb(15, 17, 21);">私网IP</font>**<font style="color:rgb(15, 17, 21);">（如</font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">192.168.1.101</font>`<font style="color:rgb(15, 17, 21);">）。它们通过一个叫</font><font style="color:rgb(15, 17, 21);"> </font>**<font style="color:rgb(15, 17, 21);">NAT</font>**<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">的技术，共享你家里那</font>**<font style="color:rgb(15, 17, 21);">一个</font>**<font style="color:rgb(15, 17, 21);">对外的</font>**<font style="color:rgb(15, 17, 21);">公网IP</font>**<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">来上网。</font>

---

### <font style="color:rgb(15, 17, 21);">总结对比</font>
| <font style="color:rgb(15, 17, 21);">概念</font>       | <font style="color:rgb(15, 17, 21);">作用</font>                | <font style="color:rgb(15, 17, 21);">唯一性</font>        | <font style="color:rgb(15, 17, 21);">例子</font> | <font style="color:rgb(15, 17, 21);">分配者</font>           |
| ---------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------ | ---------------------------------------------- | --------------------------------------------------------- |
| **<font style="color:rgb(15, 17, 21);">IPv4</font>** | <font style="color:rgb(15, 17, 21);">当前主流的互联网通信协议</font>      | <font style="color:rgb(15, 17, 21);">协议本身</font>       | 192.168.1.1                                    | <font style="color:rgb(15, 17, 21);">协议标准</font>          |
| **<font style="color:rgb(15, 17, 21);">IPv6</font>** | <font style="color:rgb(15, 17, 21);">下一代互联网通信协议，解决地址枯竭</font> | <font style="color:rgb(15, 17, 21);">协议本身</font>       | 2001:db8::1                                    | <font style="color:rgb(15, 17, 21);">协议标准</font>          |
| **<font style="color:rgb(15, 17, 21);">公网IP</font>** | <font style="color:rgb(15, 17, 21);">在互联网上标识一个设备/网络</font>    | **<font style="color:rgb(15, 17, 21);">全球唯一</font>**   | 120.132.45.67                                  | <font style="color:rgb(15, 17, 21);">互联网服务提供商(ISP)</font> |
| **<font style="color:rgb(15, 17, 21);">私网IP</font>** | <font style="color:rgb(15, 17, 21);">在局域网内部标识一个设备</font>      | **<font style="color:rgb(15, 17, 21);">局域网内唯一</font>** | 192.168.1.101                                  | <font style="color:rgb(15, 17, 21);">本地路由器</font>         |


