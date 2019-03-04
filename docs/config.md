# 通过Nginx部署Django

Django的部署可以有很多方式，采用nginx+uwsgi的方式是其中比较常见的一种方式。

在这种方式中，我们的通常做法是，将nginx作为服务器最前端，它将接收WEB的所有请求，统一管理请求。nginx把所有静态请求自己来处理（这是NGINX的强项）。然后，NGINX将所有非静态请求通过uwsgi传递给Django，由Django来进行处理，从而完成一次WEB请求。

可见，uwsgi的作用就类似一个桥接器。起到桥梁的作用。

##  安装nginx

###  配置ISO作为yum源

可以在官网下载nginx来安装，但是同时需要安装一系列的依赖文件，依赖文件需使用yum来安装，否则安装会极为繁琐！在安装之前首先要配置yum源（因为无法访问互联网）。

1.挂载ISO文件

```
mkdir /media/CentOS
mount /dev/sr0 /media/CentOS
```

2.修改repo文件

```
vi /etc/yum.repos.d/Centos-Media.repo
```

```
name=CentOS-$releasever - Media
baseurl=file:///media/CentOS/ #把默认的baseurl注释或者删除
gpgcheck=0  #这条最重要
```

3.将Centos-base.repo改名

```
cd /etc/yum.repos.d
mv Centos-Base.repo Centos-Base.repo.bak
```

4.查看yum源是否启用

   ```
yum repolist all
   ```

​     未启用的话使用如下命令启用

   ```
yum-config-manager --enable c6-media  #其中cd-media为Centos-Media.repo文件中的标识
   ```

5.刷新yum源

   ```
yum clean all
yum list #查看yum源是否可用
   ```

### 开始安装nginx

  系统平台：Centos6.8 64位

1. 安装编译工具及库文件

   ```
   yum -y install make zlib zlib-devel gcc-c++ libtool openssl openssl-devel
   ```

2. 安装PCRE

   > PCRE的作用是让Nginx支持Rewrit功能,pcre是编译nginx时必要的文件

   - 下载并上传pcre安装包
     下载地址：[http://sourceforge.net/projects/pcre/files/pcre](http://sourceforge.net/projects/pcre/files/pcre)

   - 解压安装包
     ```
     tar -zvxf pcre-8.42.tar.gz
     ```

   - 进入安装包目录编译安装

     ```
     cd pcre-8.42
     ./ configure
     make && make install
     ```

   - 查看pcre版本检查是否安装成功
     ```
     pcre-config --version
     ```

3. 安装nginx

   - 下载并上传nginx安装包
     下载地址:[http://www.nginx.org](http://www.nginx.org)

   - 解压安装包

     ```
     tar -zxvf nginx-1.14.2.tar.gz
     ```

   - 进入安装目录编译安装
     ```
     cd nginx-1.14.2
     ./configure --prefix=/usr/local/webserver/nginx  --with-pcre=../pcre-8.42
     make && make install
     ```

   - 查看nginx版本检查是否安装成功

     ```
     /usr/local/webserver/nginx/sbin/nginx -v
     ```


###  配置Nginx

1.修改nginx的配置文件，配置文件位于`/usr/local/webserver/nginx/conf/nginx.conf`

```shell
 server {
    listen       8088;    # 修改端口号
    server_name  localhost;

    #charset koi8-r; 

    #access_log  logs/host.access.log  main;

    location / {
        root   html;
        index  index.html index.htm;
    }
```

2.检查配置文件nginx.conf是否正确

```shell
/usr/local/webserver/nginx/sbin/nginx -t
```

3.启动nginx
```shell
/usr/local/webserver/nginx/sbin/nginx
```
4.查看nginx是否启动成功
```shell
netstat -tlap | grep 8080
```

> 可以将nginx目录添加为环境变量，这样以后启动时就不用每次填写绝对路径

5.关闭防火墙

```shell
service iptables stop
```

## 安装uwsgi

在安装uwsgi之前请先安装**python3.6**

安装前请将pip源更换为H3C内部地址，pip源设置如下：

```python
[global]
trusted-host = rdmirrors.h3c.com
index-url = http://rdmirrors.h3c.com/pypi/web/simple
find-links = http://rdmirrors.h3c.com/pypi/web

[install]
find-links = http://rdmirrors.h3c.com/pypi/web
```

**<del>内网linux服务器无法访问H3C内部pip地址</del>**

**解决办法：**

- 在本地电脑上使用`pip  download -d pipPackages -r uwsgi`将环境依赖文件导入到pipPackages文件夹内。
- 将pipPackages文件夹上传到服务器上，在使用`pip install --no-index --find-links=pipPackages/ uwsgi`

### 配置uwsgi

在项目根目录中新建文件uwsgi.ini，写入以下配置：

```shell
[uwsgi]
# Django-related settings
# Django项目本地端口
socket = 0.0.0.0:8000
# 项目根目录位置
chdir = /var/www/Eshare
# wsgi.py文件在项目的中的相对位置
wsgi-file = Eshare/wsgi.py
module =blog.wsgi
# 进程设置，无需变动
# master
master = true
# maximum number of worker processes
# 启动4个uwsgi进程
processes = 4
# ... with appropriate permissions - may be needed
# chmod-socket    = 664
# clear environment on exit
vacuum = true
pidfile=uwsgi.pid
daemonize=uwsgi.log
```

**常用uwsgi命令:**

```shell
启动：uwsgi --ini uwsgi.ini #使用刚才创建的uwsgi.ini启动，启动后会自动拉起django
停止：uwsgi --stop uwsgi.pid
重启：uwsgi --reload uwsgi.pid
```

### 修改nginx配置文件

由于安装了uwsgi，所以要在nginx中和uwsgi联动，使得nginx可以做uwsgi的反向代理。

配置文件总体如下：

```shell
user  root;
worker_processes  4;

error_log  /usr/local/webserver/nginx/logs/nginx_error.log crit;

pid       /usr/local/webserver/nginx/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';


    sendfile        on;
    tcp_nopush     on;

    keepalive_timeout  65;

    gzip  on;

    server {
        listen       80;
        server_name  localhost;

        location / {
            include uwsgi_params;
            uwsgi_pass 127.0.0.1:8000;
            uwsgi_read_timeout 2;
        }

        location /static {
                alias /var/www/Eshare/static;
                        }

        location /media {
                alias /var/www/Eshare/media;
                        }
       }
}
```

## 注意事项

每次修改了Django项目中的模板/视图/URL/配置文件，都需要重启uwsgi服务。
修改Nginx配置文件，都需要重启Nginx服务。
这里提供一个重启脚本 

```shell
killall -9 uwsgi; 杀死uwsgi服务
cd /var/www/Eshare/Eshare;
uwsgi --ini /var/www/Eshare/Eshare/uwsgi.ini;
nginx -s reload;  重启nginx  
```

后台无样式的话，需要在settings.py中添加：

```shell
STATIC_ROOT = '/var/www/Eshare/static/'
```

然后执行命令：`python manage.py collectstatic`

