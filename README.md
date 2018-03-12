# Flask_Building-_Python_Web_Services

更新apt-get
```
sudo apt-get update
sudo apt-get upgrade
```

安装python3
```
sudo apt-get install python3
```
安装pip3
```
sudo apt-get install python3-pip
```

安装flask
```
sudo pip3 install flask
```
安装python的pymysql三方库
```
sudo pip3 install pymysql
```

安装：mysql-server
```
sudo apt-get install mysql-server
```
安装apache2
```
sudo apt-get install apache2  apache2-doc
```
安装mod_wsgi
```
sudo apt-get install libapache2-mod-wsgi-py3
```

给账号添加目录权限
```
sudo chown -R ubuntu /etc/apache2
```
查找mod_wsgi.so文件
```
sudo find / -name mod_wsgi.so
```
/usr/lib/apache2/modules/mod_wsgi.so

编辑httpd.conf 文件
vim /etc/apache2/httpd.conf 
```
LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so
```


配置需要修改两个文件
```
touch /var/www/firstapp/hello.wsgi
touch /etc/apache2/sites-available/hello.conf
```
hello的配置

vim /var/www/firstapp/hello.wsgi
```
#/usr/bin/python3

import sys

sys.path.insert(0, "/var/www/firstapp")
from hello import app as application
```
vim /etc/apache2/sites-available/hello.conf
```
<VirtualHost *> 
ServerName example.com 
WSGIScriptAlias / /var/www/firstapp/hello.wsgi 
WSGIDaemonProcess hello 
<Directory /var/www/firstapp> 
    WSGIProcessGroup hello 
    WSGIApplicationGroup %{GLOBAL} 
    Order deny,allow 
    allow from all 
</Directory> 
</VirtualHost>
```

crimemap的配置
vim /etc/apache2/sites-available/crimemap.conf
```
<VirtualHost *>
ServerName example.com
WSGIScriptAlias / /var/www/crimemap/crimemap.wsgi
WSGIDaemonProcess crimemap
<Directory /var/www/crimemap>
    WSGIProcessGroup crimemap
    WSGIApplicationGroup %{GLOBAL}
    Order deny,allow 
    allow from all 
</Directory>
</VirtualHost>
```

vim /var/www/crimemap/crimemap.wsgi
```
#/usr/bin/python3

import sys

sys.path.insert(0, "/var/www/crimemap")
from crimemap import app as application
```

注册站点
```
sudo a2dissite 000-default.conf 
sudo a2ensite hello.conf 
```

重启apache2
```
sudo service apache2 reload
```

启动：
```
sudo service apache2 start  或者
sudo apachectl start
```


停止：
```
sudo service apache2 stop 或者
sudo apachectl stop
```

重启：
```
sudo service spache2 restart 或者
sudo apachectl restart
```
apache2的相关目录
可执行程序在以下目录：
```
/usr/sbin/apache2
```
配置文件是在以下目录
```
/etc/apache2
```
网站(web)文件是在以下目录：
```
/var/www
```
