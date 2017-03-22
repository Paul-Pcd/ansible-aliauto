# 使用ansible创建阿里云资源



安装配置ansible，[参考链接](http://marshal.ohtly.com/2017/03/13/getting-started-with-ansible/)

clone项目到本地



### 使用ansible自定义module实现的通过阿里云api为阿里云SLB上传证书

修改/roles/aliapi/defaults/main.yml中内容为自己阿里云相关配置信息

运行

```

ansible-playbook aliapi.yml --connection=local

```

###  使用ansible自定义module实现的通过阿里云python sdk为阿里云SLB上传证书

安装阿里云python sdk

```
pip install aliyunsdkcore
pip install aliyunsdkslb

```

修改/roles/alisdk/defaults/main.yml中内容为自己阿里云相关配置信息

运行

```

ansible-playbook alisdk.yml --connection=local

```
