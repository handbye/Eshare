# Generated by Django 2.1.5 on 2019-01-17 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0006_auto_20190117_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='storagedevice',
            name='model',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='存储设备型号'),
        ),
    ]
