# Generated by Django 2.2.4 on 2019-08-02 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vip', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VipPerissions',
            new_name='VipPerission',
        ),
        migrations.AlterModelTable(
            name='vip',
            table='vips',
        ),
    ]
