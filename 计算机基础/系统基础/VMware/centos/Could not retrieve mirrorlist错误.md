Could not retrieve mirrorlist ... centos-sclo-rh 报错
核心原因是 ‌CentOS 7 已于 2024 年 6 月 30 日停止官方维护（EOL）‌，导致默认的官方镜像列表地址 mirrorlist.centos.org 失效或无法解析。同时，您的系统中启用了 SCLo（Software Collections）仓库，该仓库的默认配置也指向了已失效的地址。
第一步：检查并修复基础网络连接
在修改源之前，必须确保服务器能正常访问互联网。
## 第一步.测试网络连通性‌
执行以下命令，看是否能 ping 通外网 IP 和域名：
```
ping -c 4 8.8.8.8       # 测试 IP 连通性
ping -c 4 www.baidu.com # 测试 DNS 解析
```
如果 ping 8.8.8.8 不通：检查虚拟机网络模式（NAT/桥接）或网卡配置（/etc/sysconfig/network-scripts/ifcfg-ens33 中 ONBOOT=yes），然后重启网络 systemctl restart network。
如果 ping 8.8.8.8 通但 ping www.baidu.com 不通：说明是 DNS 问题。编辑 /etc/resolv.conf，添加以下内容：
```
nameserver 8.8.8.8
nameserver 114.114.114.114
```

‌## 2.安装必要工具（可选）‌
如果后续步骤需要用到 curl 或 wget 但系统未安装，且当前 yum 不可用，可尝试先通过以下方式安装（若网络已通但 yum 报错，可跳过此步直接进行第二步换源，因为换源后 yum 即可恢复）：
```
yum install -y curl wget yum-utils
```
注：如果此时 yum 仍报错，请直接进入第二步，使用 curl 下载新源文件（通常最小化安装也自带 curl）。

## 第二步：更换 CentOS 7 基础源为阿里云镜像
由于官方源已停用，必须将基础源（Base/Updates/Extras）替换为国内可用的镜像源（如阿里云、清华源等）。这里以阿里云为例。
1.备份原有源文件
```
cd /etc/yum.repos.d/
mkdir backup
mv *.repo backup/
```
‌2.下载阿里云 CentOS 7 源配置文件‌
使用 curl 下载新的 repo 文件：
```
curl -o /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-7.repo
```
如果提示 curl 不存在，且无法安装，请手动在另一台机器下载该文件并上传至服务器对应目录。
3.清理缓存并生成新缓存
```
yum clean all
yum makecache
```
此时，基础的 yum install 应该已经可以正常工作。但如果您的业务依赖 SCL 软件包（如 rh-python36, devtoolset-7 等），仍需执行第三步。

## 第三步：修复 SCLo (Software Collections) 源
报错信息明确指向 centos-sclo-rh，这是因为 SCLo 仓库的配置文件仍指向官方已下线的地址。您需要单独修复这两个文件：CentOS-SCLo-scl.repo 和 CentOS-SCLo-scl-rh.repo。
1.恢复或创建 SCLo 源文件‌
确保 /etc/yum.repos.d/ 目录下存在 CentOS-SCLo-scl.repo 和 CentOS-SCLo-scl-rh.repo。如果之前备份到了 backup 文件夹，可以复制回来修改，或者直接新建。

2.编辑 CentOS-SCLo-scl-rh.repo‌
```
vi /etc/yum.repos.d/CentOS-SCLo-scl-rh.repo
```
将内容替换为以下阿里云地址（注释掉原有的 mirrorlist，启用 baseurl）：
```
[centos-sclo-rh]
name=CentOS-7 - SCLo rh
baseurl=https://mirrors.aliyun.com/centos/7/sclo/$basearch/rh/
gpgcheck=1
enabled=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-SIG-SCLo

[centos-sclo-rh-testing]
name=CentOS-7 - SCLo rh Testing
baseurl=https://mirrors.aliyun.com/centos/7/sclo/$basearch/rh/
gpgcheck=0
enabled=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-SIG-SCLo
```

3.编辑 CentOS-SCLo-scl.repo‌
```
vi /etc/yum.repos.d/CentOS-SCLo-scl.repo
```
将内容替换为：
```
[centos-sclo-sclo]
name=CentOS-7 - SCLo sclo
baseurl=https://mirrors.aliyun.com/centos/7/sclo/$basearch/sclo/
gpgcheck=1
enabled=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-SIG-SCLo
```

‌4.清理缓存并重建
```
yum clean all
yum makecache

```
## 第四步：验证修复结果
执行以下命令检查仓库状态：
```
yum repolist
```
如果输出中不再出现错误，且能看到 base、updates、extras 以及（如果启用了）centos-sclo-rh 等仓库 ID，说明修复成功。
您可以尝试安装一个小软件进行测试：
```
yum install -y vim-enhanced
```


