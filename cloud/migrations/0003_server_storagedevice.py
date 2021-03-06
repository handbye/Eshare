# Generated by Django 2.1.5 on 2019-01-16 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0002_asset'),
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_asset_type', models.SmallIntegerField(choices=[(0, 'CAS'), (1, 'UIS'), (2, 'CloudOs'), (3, 'CloudClass')], default=0, verbose_name='服务器类型')),
                ('os_type', models.CharField(blank=True, max_length=64, null=True, verbose_name='操作系统类型')),
                ('os_release', models.CharField(blank=True, max_length=64, null=True, verbose_name='操作系统版本')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cloud.Asset')),
                ('hosted_on', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hosted_on_server', to='cloud.Server', verbose_name='宿主机')),
            ],
            options={
                'verbose_name': '服务器',
                'verbose_name_plural': '服务器',
            },
        ),
        migrations.CreateModel(
            name='StorageDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cloud.Asset')),
            ],
            options={
                'verbose_name': '存储设备',
                'verbose_name_plural': '存储设备',
            },
        ),
    ]
