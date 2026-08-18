‌解决方案步骤‌
```
‌1. 检查并启动 NetworkManager 服务
# 查看服务状态
systemctl status NetworkManager
若为 active服务启动

#启动服务
systemctl start NetworkManager
# 设置开机自启
systemctl enable NetworkManager
# 重启服务以应用更改
systemctl restart NetworkManager

‌2. 修改网卡配置文件
# 进入网卡配置目录
cd /etc/sysconfig/network-scripts/
# 查看网卡文件名（通常为 ifcfg-ens33）
ls ifcfg-*
# 编辑配置文件
vim  ifcfg-ens33
若 ONBOOT=no 或 NM_CONTROLLED=no，必须修改为 yes

保存并退出后执行
# 重载网络配置
nmcli connection reload
# 重启网络服务
systemctl restart NetworkManager

‌3. 检查并启用 VMware 宿主机服务（Windows）‌
按 Win + R，输入 services.msc 回车
找到以下服务，确保状态为 ‌“正在运行”‌，启动类型为 ‌“自动”‌：
VMware DHCP Service
VMware NAT Service
若未运行，右键 → 启动
```

