from django.contrib import admin
from cloud import  models

@admin.register(models.Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['asset_type','name','business_unit','status','manage_ip','user','c_time','m_time']
    search_fields = ('user','manage_ip','name')
    list_filter = ['asset_type','status','user','c_time','m_time']

@admin.register(models.Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ['sub_asset_type','os_type','os_release','cpu_count','cpu_core_count','capacity']
    search_fields = ('sub_asset_type','os_type','os_release')
    list_filter = ['sub_asset_type','os_type','os_release']

@admin.register(models.StorageDevice)
class StorageAdmin(admin.ModelAdmin):
    list_display = ['asset','storage_name','model','memo']


@admin.register(models.NetworkDevice)
class NetworkAdmin(admin.ModelAdmin):
    list_display = ['sub_asset_type', 'model']

@admin.register(models.BusinessUnit)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['sub_asset_type', 'name']

admin.site.site_header = 'Eshare'
admin.site.site_title = 'Eshare'