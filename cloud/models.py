from django.db import models
from django.contrib.auth.models import User

class Asset(models.Model):
    asset_type_choice = (
        ('server', '服务器'),
        ('networkdevice', '网络设备'),
        ('storagedevice', '存储设备'),
    )
    asset_status=(
        (0,'在线'),
        (1,'下线'),
        (2,'故障'),
    )
    asset_type = models.CharField(choices=asset_type_choice,max_length=64,default='server',verbose_name='资产类型')
    name = models.CharField(max_length=64,unique=True,verbose_name='资产名称')
    business_unit=models.ForeignKey('BusinessUnit',null=True,blank=True,verbose_name='所属产品线',on_delete=models.DO_NOTHING)
    status = models.SmallIntegerField(choices=asset_status,default=0,verbose_name='设备状态')
    manage_ip = models.GenericIPAddressField(null=True,blank=True,verbose_name='管理IP')
    memo = models.CharField(max_length=128,null=True,blank=True,verbose_name='备注')
    user = models.ForeignKey(User,null=True,blank=True,verbose_name='使用者',on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True,verbose_name='创建日期')
    m_time = models.DateTimeField(auto_now=True,verbose_name='更新日期')

    def __str__(self):
        return '[%s] %s' %(self.get_asset_type_display(),self.name)
    class Meta:
        verbose_name='资产总表'
        verbose_name_plural='资产总表'
        ordering=['-c_time','-m_time']


class Server(models.Model):
    sub_asset_type_choice = (
        (0,'CAS'),
        (1,'UIS'),
        (2,'CloudOs'),
        (3,'CloudClass'),
        (4,'UIS企业版'),
        (5, '其它'),
    )
    asset = models.OneToOneField('Asset',on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice,default=0,verbose_name='服务器类型')
    hosted_on = models.ForeignKey('self',related_name='hosted_on_server',blank=True,null=True,verbose_name='宿主机',on_delete=models.CASCADE)
    os_type = models.CharField(max_length=64,blank=True,null=True,verbose_name='操作系统类型')
    os_release = models.CharField(max_length=64,blank=True,null=True,verbose_name='操作系统版本')
    cpu_count = models.PositiveSmallIntegerField(verbose_name='物理CPU个数', default=1, null=True, blank=True)
    cpu_core_count = models.PositiveIntegerField(verbose_name='CPU核数', default=1, null=True, blank=True)
    capacity = models.IntegerField(blank=True, null=True, verbose_name='内存大小(GB)')

    def __str__(self):
        return '%s--%s' %(self.get_sub_asset_type_display(),self.os_release)
    class Meta:
        verbose_name='服务器'
        verbose_name_plural='服务器'


class StorageDevice(models.Model):
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    storage_name = models.CharField(null=True,blank=True,max_length=64,verbose_name='设备名')
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name="存储设备型号")
    memo = models.TextField(null=True,blank=True,verbose_name='备注')
    def __str__(self):
        return self.asset.name
    class Meta:
        verbose_name='存储设备'
        verbose_name_plural='存储设备'


class NetworkDevice(models.Model):
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type_choice = (
        (0, '交换机'),
        (1, '路由器'),
        (2, '防火墙'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice,default=0,verbose_name='网络设备类型')
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name="网络设备型号")
    def __str__(self):
        return '%s--%s--%s' %(self.asset.name,self.get_sub_asset_type_display(),self.model)
    class Meta:
        verbose_name='网络设备'
        verbose_name_plural='网络设备'



class BusinessUnit(models.Model):
    sub_asset_type_choice = (
        (0, '云计算'),
        (1, '网络'),
        (2, '安全'),
        (3, '其他'),
    )
    name = models.CharField(verbose_name='名称', max_length=64, unique=True)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='所属产品线')
    def __str__(self):
        return '%s(%s)'%(self.get_sub_asset_type_display(),self.name)
    class Meta:
        verbose_name = '产品线'
        verbose_name_plural = "产品线"
