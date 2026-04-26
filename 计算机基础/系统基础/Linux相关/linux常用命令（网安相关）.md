## <font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">⌨️</font><font style="color:rgb(15, 17, 21);">快捷键（终端操作）</font>
| ctrl+R | 搜索历史命令 |
| --- | --- |
| ctrl+L | 清屏，清除上方命令 |
| ctrl+C | 终止当前命令 |
| ctrl+Z | 暂停当前内容 |
| ctrl+U | 删除光标之前所有内容 |
| ctrl+K | 删除光标之后所有内容 |
| ctrl+W | 以分隔符为单位删除 |
| ctrl+Y | 粘贴刚才删除的内容（ctrl+U/K/W的反向操作） |
| ctrl+A | 跳转到行首 |
| ctrl+E | 跳转到行尾 |


## <font style="color:rgb(15, 17, 21);">🔍</font><font style="color:rgb(15, 17, 21);"> 系统信息与权限</font>
| <font style="color:rgb(15, 17, 21);">命令</font> | <font style="color:rgb(15, 17, 21);">说明</font>                 |
| ---------------------------------------------- | -------------------------------------------------------------- |
| whoami                                         | <font style="color:rgb(15, 17, 21);">查看当前用户名（判断当前权限）</font>    |
| hostname                                       | <font style="color:rgb(15, 17, 21);">查看当前主机名</font>            |
| pwd                                            | <font style="color:rgb(15, 17, 21);">显示当前所在路径</font>           |
| which <文件>                                     | <font style="color:rgb(15, 17, 21);">查找文件路径</font>             |
| sudo <命令>                                      | <font style="color:rgb(15, 17, 21);">以高权限执行命令</font>           |
| su root                                        | <font style="color:rgb(15, 17, 21);">切换到 root 用户</font>        |
| su <用户名>                                       | <font style="color:rgb(15, 17, 21);">切换到指定用户（降权）</font>        |
| chmod 755 <文件>                                 | <font style="color:rgb(15, 17, 21);">设置权限：所有者 rwx，其他 rx</font> |
| chmod a+x <文件>                                 | <font style="color:rgb(15, 17, 21);">给所有用户添加执行权限</font>        |
| chown                                          | <font style="color:rgb(15, 17, 21);">修改文件所有者</font>            |
| chgrp                                          | <font style="color:rgb(15, 17, 21);">修改文件所属组</font>            |

### <font style="color:rgba(0, 0, 0, 0.9);">chmod补充：权限模式参数</font>
#### <font style="color:rgba(0, 0, 0, 0.9);">1. 数字模式（八进制模式）</font>
<font style="color:rgb(0, 0, 0);">最常用的方式，使用3位八进制数表示权限：</font>

| <font style="color:rgb(0, 0, 0);">数字</font> | <font style="color:rgb(0, 0, 0);">权限</font> | <font style="color:rgb(0, 0, 0);">说明</font>       |
| :------------------------------------------ | :------------------------------------------ | :------------------------------------------------ |
| 0                                           | ---                                         | <font style="color:rgb(0, 0, 0);">无任何权限</font>    |
| 1                                           | --x                                         | <font style="color:rgb(0, 0, 0);">只有执行权限</font>   |
| 2                                           | -w-                                         | <font style="color:rgb(0, 0, 0);">只有写权限</font>    |
| 3                                           | -wx                                         | <font style="color:rgb(0, 0, 0);">写和执行权限</font>   |
| 4                                           | r--                                         | <font style="color:rgb(0, 0, 0);">只有读权限</font>    |
| 5                                           | r-x                                         | <font style="color:rgb(0, 0, 0);">读和执行权限</font>   |
| 6                                           | rw-                                         | <font style="color:rgb(0, 0, 0);">读和写权限</font>    |
| 7                                           | rwx                                         | <font style="color:rgb(0, 0, 0);">读、写、执行权限</font> |

**<font style="color:rgb(0, 0, 0);">数字模式结构：</font>**

```plain
chmod ABC file
```

+ A= 用户(User/Owner)权限
+ B= 组(Group)权限
+ C= 其他用户(Other)权限

**示例：**

```plain
chmod 755 script.sh    # 用户:rwx, 组:r-x, 其他:r-x
chmod 644 document.txt # 用户:rw-, 组:r--, 其他:r--
chmod 700 private.txt  # 只有用户有全部权限，其他用户无任何权限
```

#### <font style="color:rgba(0, 0, 0, 0.9);">2. 符号模式（字母模式）</font>
<font style="color:rgb(0, 0, 0);">更直观的方式，使用字母表示权限：</font>

**<font style="color:rgb(0, 0, 0);">用户类别：</font>**

+ u: 文件所有者(User)
+ g: 文件所属组(Group)
+ o: 其他用户(Other)
+ a: 所有用户(All)，相当于ugo

**<font style="color:rgb(0, 0, 0);">操作符号：</font>**

+ +: 添加权限
+ -: 移除权限
+ =: 设置精确权限（覆盖原有权限）

**<font style="color:rgb(0, 0, 0);">权限类型：</font>**

+ r: 读权限
+ w: 写权限
+ x: 执行权限

**<font style="color:rgb(0, 0, 0);">符号模式示例：</font>**

```plain
# 添加执行权限给所有用户
chmod a+x script.sh

# 给文件所有者添加写权限
chmod u+w file.txt

# 移除组和其他用户的写权限
chmod go-w document.txt

# 设置精确权限：用户有全部权限，组有读权限，其他用户无权限
chmod u=rwx,g=r,o= file.txt

# 组合操作
chmod u+x,go-rwx secret.txt
```

## <font style="color:rgb(15, 17, 21);">📁</font><font style="color:rgb(15, 17, 21);"> 文件与目录操作</font>
| <font style="color:rgb(15, 17, 21);">命令</font> | <font style="color:rgb(15, 17, 21);">说明</font>                                                                                         | <font style="color:rgb(15, 17, 21);">扩充</font>                                                                                                                                                                                                                                              |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ls                                             | <font style="color:rgb(15, 17, 21);">列出目录内容</font>                                                                                     | <font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">ls -a </font><font style="color:rgb(15, 17, 21);">显示所有文件（包括隐藏）</font><br/><font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">ls -l </font><font style="color:rgb(15, 17, 21);">显示详细信息</font> |
| cd                                             | <font style="color:rgb(15, 17, 21);">切换目录</font>                                                                                       | <font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">cd .. </font><font style="color:rgb(15, 17, 21);">返回上一级</font><br/><font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">cd ~</font><font style="color:rgb(15, 17, 21);">回到家目录</font>           |
| mkdir                                          | <font style="color:rgb(15, 17, 21);">创建目录</font>                                                                                       | <font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">mkdir -p</font><font style="color:rgb(15, 17, 21);">递归创建目录</font>                                                                                                                                                  |
| touch                                          | <font style="color:rgb(15, 17, 21);">创建文件</font>                                                                                       | <font style="color:rgb(15, 17, 21);"></font>                                                                                                                                                                                                                                                |
| cp <源> <目标>                                    | <font style="color:rgb(15, 17, 21);">复制文件/目录</font>                                                                                    | <font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">cp -r 1/ 2/</font><font style="color:rgb(15, 17, 21);">拷贝1目录到2目录</font>                                                                                                                                            |
| mv <源> <目标>                                    | <font style="color:rgb(15, 17, 21);">移动或重命名</font>                                                                                     | <font style="color:rgb(15, 17, 21);"></font>                                                                                                                                                                                                                                                |
| rm                                             | <font style="color:rgb(15, 17, 21);"></font><font style="color:rgb(15, 17, 21);">删除文件</font><font style="color:#DF2A3F;">（谨慎使用）</font> | <font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">rm -r</font><font style="color:rgb(15, 17, 21);">删除文件夹</font><br/>                                 rm -f强制删除<br>rm -rf /*﻿﻿强制删除根目录所有文件                                                                             |
| ./                                             | <font style="color:rgb(15, 17, 21);">引用当前目录</font>                                                                                     | <font style="color:rgb(15, 17, 21);"></font>                                                                                                                                                                                                                                                |
| ../                                            | <font style="color:rgb(15, 17, 21);">引用上级目录</font>                                                                                     | <font style="color:rgb(15, 17, 21);"></font>                                                                                                                                                                                                                                                |
| du                                             | <font style="color:rgb(15, 17, 21);">计算磁盘使用情况</font>                                                                                   | `du -a`显示所有文件的使用<br>`du -s`仅显示总占用大小<br>`du -h`人性化显示（K/M/G单位）-h：human readable                                                                                                                                                                                                               |

### du和du *核心区别对比

| <font style="color:rgb(0, 0, 0);">命令</font> | <font style="color:rgb(0, 0, 0);">作用对象</font> | <font style="color:rgb(0, 0, 0);">输出内容</font>                                                       | <font style="color:rgb(0, 0, 0);">适用场景</font>               |
| :------------------------------------------ | :-------------------------------------------- | :-------------------------------------------------------------------------------------------------- | :---------------------------------------------------------- |
| du                                          | 当前目录本身                                        | <font style="color:rgb(0, 0, 0);">当前目录的</font>**<font style="color:rgb(0, 0, 0);">总磁盘使用量</font>**   | <font style="color:rgb(0, 0, 0);">查看整个目录占用了多少空间</font>      |
| du *                                        | 当前目录下的所有子项                                    | <font style="color:rgb(0, 0, 0);">每个文件和子目录的</font>**<font style="color:rgb(0, 0, 0);">单独大小</font>** | <font style="color:rgb(0, 0, 0);">查看目录内哪些文件/子目录占用了空间</font> |


## <font style="color:rgb(15, 17, 21);">📄</font><font style="color:rgb(15, 17, 21);"> 文件查看与编辑</font>
| 命令        | 说明                                                       | 扩充                                                                                                                                             |
| --------- | -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| cat <文件>  | <font style="color:rgb(15, 17, 21);">读取文件内容，打印到终端</font> | <font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">cat -n </font><font style="color:rgb(15, 17, 21);">显示行号</font>        |
| less <文件> | <font style="color:rgb(15, 17, 21);">分页查看</font>         | <font style="color:rgb(15, 17, 21);">按b上一页，按空格下一页,按d下半页，按=看进度，按/加内容搜索加标亮内容</font>                                                              |
| head <文件> | <font style="color:rgb(15, 17, 21);">默认显示前10行</font>     | <font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">head -n 数字</font><font style="color:rgb(15, 17, 21);"> 指定显示前n行</font> |
| tail <文件> | <font style="color:rgb(15, 17, 21);">默认显示后10行</font>     | <font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">tail -n 数字 </font><font style="color:rgb(15, 17, 21);">指定显示后n行</font> |
| vim       | <font style="color:rgb(15, 17, 21);">多模式文本编辑器</font>     | <font style="color:rgb(15, 17, 21);"></font>                                                                                                   |


## <font style="color:rgb(15, 17, 21);">🔗</font><font style="color:rgb(15, 17, 21);"> 链接</font>
| <font style="color:rgb(15, 17, 21);">命令</font> | <font style="color:rgb(15, 17, 21);">说明</font>                  | <font style="color:rgb(15, 17, 21);">扩充</font>                                                                                                  |
| ---------------------------------------------- | --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| ln <源> <目标>                                    | <font style="color:rgb(15, 17, 21);">创建硬链接,一个已存在的连接一个新建的</font> | <font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">ln -s <源> <目标></font><font style="color:rgb(15, 17, 21);">创建软链接</font> |


## <font style="color:rgb(15, 17, 21);">👥</font><font style="color:rgb(15, 17, 21);"> 用户与组管理</font>
| <font style="color:rgb(15, 17, 21);">命令</font> | <font style="color:rgb(15, 17, 21);">说明</font>                                                                 |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| useradd <用户>                                   | <font style="color:rgb(15, 17, 21);">创建用户</font>                                                               |
| userdel <用户>                                   | <font style="color:rgb(15, 17, 21);">删除用户</font>                                                               |
| usermod -g <新组名> <用户名>                         | <font style="color:rgb(15, 17, 21);">修改用户主组</font>                                                             |
| usermod -G <新组名> <用户名>                         | <font style="color:rgb(15, 17, 21);">添加用户到附加组</font>                                                           |
| sudo usermod -aG <附加组名> <用户>                   | <font style="color:rgb(15, 17, 21);">追加用户到组（</font>-a 表追加，避免覆盖原有组<font style="color:rgb(15, 17, 21);">）</font> |
| groupadd <组>                                   | <font style="color:rgb(15, 17, 21);">创建组</font>                                                                |
| groupdel <组>                                   | <font style="color:rgb(15, 17, 21);">删除组</font>                                                                |
| groups <用户>                                    | <font style="color:rgb(15, 17, 21);">查看用户所属组，查看用户权限</font>                                                     |
| getent group                                   | <font style="color:rgb(15, 17, 21);">查看所有组</font>                                                              |

## <font style="color:rgb(15, 17, 21);">📂</font><font style="color:rgb(15, 17, 21);"> 查找与统计</font>
| <font style="color:rgb(15, 17, 21);">命令</font> | <font style="color:rgb(15, 17, 21);">说明</font>                 |
| ---------------------------------------------- | -------------------------------------------------------------- |
| find / -name "*.sh"                            | <font style="color:rgb(15, 17, 21);">在根目录查找所有 .sh 文件</font>    |
| find /var -size -5M                            | <font style="color:rgb(15, 17, 21);">在var中查找小于 5MB 的文件</font>  |
| find / -atime -7                               | <font style="color:rgb(15, 17, 21);">查找7天内访问过的文件</font>        |
| find -type f/d/l                               | <font style="color:rgb(15, 17, 21);">按类型查找（文件f/目录d/链接l）</font> |
| wc <文件>                                        | <font style="color:rgb(15, 17, 21);">统计行数、单词数、字节数</font>       |
| wc -l                                          | <font style="color:rgb(15, 17, 21);">仅统计行数</font>              |
| wc -w                                          | <font style="color:rgb(15, 17, 21);">仅统计单词数</font>             |
| wc -c                                          | <font style="color:rgb(15, 17, 21);">仅统计字节数</font>             |

##  文本处理与过滤

| 命令                     | 说明         | 扩充                                                                                                                                                                                                                                                                                                                                                                         |
| ---------------------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| echo                   | 输出文本或变量内容  |                                                                                                                                                                                                                                                                                                                                                                            |
| `grep "关键词" <文件>`      | 筛选，搜索关键词   | `grep -i`忽略大小写                                                                         grep -n显示行号                                                                              grep -v搜索显示不匹配的行                                                          <font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">grep -r "hello" /etc</font>查看目录以及子目录所有的 |
| `sort <文件>`            | 排序文件内容     | sort -o把排序之后的保存下来<br>sort -r反向排序<br>sort -R随机排序<br>sort -n数值排序,从小到大                                                                                                                                                                                                                                                                                                        |
| `uniq <文件>`            | 去除连续重复行    |                                                                                                                                                                                                                                                                                                                                                                            |
| `cut -c 2-4 <文件>`      | 截取第2-4列字符  |                                                                                                                                                                                                                                                                                                                                                                            |
| `cut -d ',' -f 1 <文件>` | 以逗号分隔，取第一列 |                                                                                                                                                                                                                                                                                                                                                                            |

## 重定向与管道

| 命令                                                                      | 说明                                                             |
| ----------------------------------------------------------------------- | -------------------------------------------------------------- |
| cut -d  '，' -f 1 name.txt >1.txt                                        | <font style="color:rgb(15, 17, 21);">输出为1.txt覆盖之前的内容</font>    |
| cut -d  '，' -f 1 name.txt>>1.txt                                        | <font style="color:rgb(15, 17, 21);">追加输出到文件1.txt</font>       |
| cut -d  '，' -f 1 name.txt 2>                                            | <font style="color:rgb(15, 17, 21);">错误输出</font>               |
| cut -d  '，' -f 1 name.txt `2>>`                                         | <font style="color:rgb(15, 17, 21);">追加错误信息</font>             |
| cut -d  '，' -f 1 name.txt2>&1                                           | <font style="color:rgb(15, 17, 21);">错误与标准输出合并</font>          |
| cat `<`文件                                                               | <font style="color:rgb(15, 17, 21);">被动读取文件</font>             |
| cat < name.txt输出name.txt（cat被动）          cat name.txt 打开name.txt（cat主动） |                                                                |
| wc -l `<<`END                                                           | <font style="color:rgb(15, 17, 21);">从标准输入读取直到 END，然后统计</font> |
| \|                                                                      | 管道：前一个命令的输出作为后一个的输入                                            |

### 重定向与管道相关题目

![[Pasted image 20260426115003.png|452]]

![[Pasted image 20260426145406.png|437]]
## <font style="color:rgb(15, 17, 21);"></font><font style="color:rgb(15, 17, 21);"> 更新与进程管理</font>
| <font style="color:rgb(15, 17, 21);">命令</font> | <font style="color:rgb(15, 17, 21);">说明</font>               |
| ---------------------------------------------- | ------------------------------------------------------------ |
| ps -ef                                         | <font style="color:rgb(15, 17, 21);">查看所有进程（执行那一刻的进程）</font> |
| ps -ef \| grep <进程>                            | 筛选进程                                                         |
| top                                            | <font style="color:rgb(15, 17, 21);">实时监控进程</font>           |
| kill                                           | <font style="color:rgb(15, 17, 21);">终止进程</font>             |
| sudo apt-get update                            | <font style="color:rgb(15, 17, 21);">更新软件包列表</font>          |
| sudo apt upgrade                               | 升级已安装软件                                                      |


