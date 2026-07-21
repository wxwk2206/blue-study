# 安装
1.在[https://old.kali.org/kali-images/](https://old.kali.org/kali-images/)中找到kali的老版本,一般为最新版本的前两个版本
![[Pasted image 20260703173844.png|458]]

2.在VMware中选择创建虚拟机，之后步骤如下
![[Pasted image 20260703173849.png|433]]
![[Pasted image 20260703173854.png|453]]

![[Pasted image 20260703173858.png|380]]
![[Pasted image 20260703173903.png|378]]
![[Pasted image 20260703173909.png|427]]
![[Pasted image 20260703173914.png|415]]
![[Pasted image 20260703173919.png|457]]
![[Pasted image 20260703173923.png|418]]
![[Pasted image 20260703173927.png|434]]
![[Pasted image 20260703173931.png|440]]
![[Pasted image 20260703173936.png|366]]

3.编辑虚拟机，使用kali的ISO映像文件
![[Pasted image 20260703173940.png|454]]

4.打开后的配置如下
![[Pasted image 20260703173944.png|483]]
![[Pasted image 20260703173948.png|476]]


![[Pasted image 20260703173953.png|449]]
![[Pasted image 20260703173957.png|434]]


![[Pasted image 20260703174001.png|421]]
![[Pasted image 20260703174006.png|465]]
![[Pasted image 20260703174010.png]]
![[Pasted image 20260703174013.png]]


![[Pasted image 20260703174016.png]]
![[Pasted image 20260703174019.png]]


![[Pasted image 20260703174021.png]]

# 换源
5.打开终端，输入sudo vim etc/apt/sources.list
![[Pasted image 20260703174025.png]]

进入之后，单击i进入编辑模式，将源换为国内源
![[Pasted image 20260703174030.png]]


![[Pasted image 20260703174035.png]]

点esc，shift加；，输入wq退出

6.使用以下指令，刷新加升级

sudo apt-get update刷新软件列表

sudo apt upgrade升级已装软件

