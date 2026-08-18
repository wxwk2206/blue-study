# 安装
1.在[https://old.kali.org/kali-images/](https://old.kali.org/kali-images/)中找到kali的老版本,一般为最新版本的前两个版本
![Pasted image 20260703173844](../../../PNG/Pasted%20image%2020260703173844.png)

2.在VMware中选择创建虚拟机，之后步骤如下
![Pasted image 20260703173849](../../../PNG/Pasted%20image%2020260703173849.png)
![Pasted image 20260703173854](../../../PNG/Pasted%20image%2020260703173854.png)

![Pasted image 20260703173858](../../../PNG/Pasted%20image%2020260703173858.png)
![Pasted image 20260703173903](../../../PNG/Pasted%20image%2020260703173903.png)
![Pasted image 20260703173909](../../../PNG/Pasted%20image%2020260703173909.png)
![Pasted image 20260703173914](../../../PNG/Pasted%20image%2020260703173914.png)
![Pasted image 20260703173919](../../../PNG/Pasted%20image%2020260703173919.png)
![Pasted image 20260703173923](../../../PNG/Pasted%20image%2020260703173923.png)
![Pasted image 20260703173927](../../../PNG/Pasted%20image%2020260703173927.png)
![Pasted image 20260703173931](../../../PNG/Pasted%20image%2020260703173931.png)
![Pasted image 20260703173936](../../../PNG/Pasted%20image%2020260703173936.png)

3.编辑虚拟机，使用kali的ISO映像文件
![Pasted image 20260703173940](../../../PNG/Pasted%20image%2020260703173940.png)

4.打开后的配置如下
![Pasted image 20260703173944](../../../PNG/Pasted%20image%2020260703173944.png)
![Pasted image 20260703173948](../../../PNG/Pasted%20image%2020260703173948.png)


![Pasted image 20260703173953](../../../PNG/Pasted%20image%2020260703173953.png)
![Pasted image 20260703173957](../../../PNG/Pasted%20image%2020260703173957.png)


![Pasted image 20260703174001](../../../PNG/Pasted%20image%2020260703174001.png)
![Pasted image 20260703174006](../../../PNG/Pasted%20image%2020260703174006.png)
![Pasted image 20260703174010](../../../PNG/Pasted%20image%2020260703174010.png)
![Pasted image 20260703174013](../../../PNG/Pasted%20image%2020260703174013.png)


![Pasted image 20260703174016](../../../PNG/Pasted%20image%2020260703174016.png)
![Pasted image 20260703174019](../../../PNG/Pasted%20image%2020260703174019.png)


![Pasted image 20260703174021](../../../PNG/Pasted%20image%2020260703174021.png)

# 换源
5.打开终端，输入sudo vim etc/apt/sources.list
![Pasted image 20260703174025](../../../PNG/Pasted%20image%2020260703174025.png)

进入之后，单击i进入编辑模式，将源换为国内源
![Pasted image 20260703174030](../../../PNG/Pasted%20image%2020260703174030.png)


![Pasted image 20260703174035](../../../PNG/Pasted%20image%2020260703174035.png)

点esc，shift加；，输入wq退出

6.使用以下指令，刷新加升级

sudo apt-get update刷新软件列表

sudo apt upgrade升级已装软件

