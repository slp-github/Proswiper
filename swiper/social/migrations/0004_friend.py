# Generated by Django 2.2.3 on 2019-07-31 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0003_auto_20190731_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid1', models.IntegerField()),
                ('uid2', models.IntegerField()),
            ],
            options={
                'db_table': 'friends',
            },
        ),
    ]