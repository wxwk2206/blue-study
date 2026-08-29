### 临时方案
选中文件，**按住 Shift 再点鼠标右键**，直接弹出完整菜单，不用点【显示更多选项】

### 永久方案
1. Win+X → **Windows 终端(管理员)**（命令提示符管理员也可以）
2. 粘贴下面命令，回车执行
```cmd
reg.exe add "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32" /f /ve
```
3. 重启资源管理器生效：
```cmd
taskkill /f /im explorer.exe & start explorer.exe
```

之后右键文件，**直接完整菜单，不再精简菜单+显示更多**

### 恢复默认（改回原版Win11精简右键）
管理员终端执行：
```cmd
reg.exe delete "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}" /va /f
```
同样重启 explorer

补充：
新版Win11 24H2、25H2 这条注册表依然有效；
修改只对当前登录用户生效，不会影响其他账户。
