# Generated by Django 2.1.5 on 2019-01-16 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='产品线')),
            ],
            options={
                'verbose_name': '产品线',
                'verbose_name_plural': '产品线',
            },
        ),
    ]
