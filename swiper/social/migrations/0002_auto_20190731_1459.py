# Generated by Django 2.2.3 on 2019-07-31 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Swiper',
            new_name='Swiped',
        ),
        migrations.AlterModelTable(
            name='swiped',
            table='swiped',
        ),
    ]
