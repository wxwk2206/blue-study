靶场放入phpstudy的D:\software\phpstudy\phpstudy_pro\WWW\目录下
![[Pasted image 20260811142003.png|581]]
php中启动apache和mysql
![[Pasted image 20260811151734.png|502]]
注意：电脑中本来就有启动MySQL服务的需要关闭原本的MySQL服务，在系统的服务中

## 1.sqli-labs
sqli-labs中进行配置
D:\software\phpstudy\phpstudy_pro\WWW\sqli-labs\sql-connections下的db-creds.inc文件改配置，密码与下图一致
```
<?php

//give your mysql connection username n password
$dbuser ='root';
$dbpass ='123456';
$dbname ="securitys";
$host = 'localhost';
$dbname1 = "challenges";



?>
```
![[Pasted image 20260811150829.png|633]]

配置一个网站，然后访问http://sqli-labs:8011就可以正常使用了
![[Pasted image 20260811150925.png|549]]

## 2.pikachu
D:\software\phpstudy\phpstudy_pro\WWW\pikachu\inc中修改config.inc.php配置
```
<?php
//全局session_start
session_start();
//全局居设置时区
date_default_timezone_set('Asia/Shanghai');
//全局设置默认字符
header('Content-type:text/html;charset=utf-8');
//定义数据库连接参数
define('DBHOST', '127.0.0.1');//将localhost或者127.0.0.1修改为数据库服务器的地址
define('DBUSER', 'root');//将root修改为连接mysql的用户名
define('DBPW', '123456');//将root修改为连接mysql的密码，如果改了还是连接不上，请先手动连接下你的数据库，确保数据库服务没问题在说!
define('DBNAME', 'pikachu');//自定义，建议不修改
define('DBPORT', '3306');//将3306修改为mysql的连接端口，默认tcp3306

?>

```
访问http://127.0.0.1/pikachu/install.php，点击安装/初始化就成功了
![[Pasted image 20260811153709.png|620]]
## 3.upload
加一个域名或者访问127.0.0.1都行
![[Pasted image 20260811153854.png|593]]
