# Generated by Django 2.2.3 on 2019-07-17 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phonenum', models.CharField(max_length=16, unique=True)),
                ('nickname', models.CharField(max_length=18)),
                ('sex', models.IntegerField(choices=[(0, '未知'), (1, '男'), (2, '女')], default=0)),
                ('birth_year', models.IntegerField(default=2000)),
                ('birth_month', models.IntegerField(default=1)),
                ('birth_day', models.IntegerField(default=1)),
                ('avatar', models.CharField(max_length=256)),
                ('location', models.CharField(choices=[('gz', '广州'), ('sz', '深圳'), ('sh', '上海'), ('cd', '成都'), ('bj', '北京'), ('cq', '重庆'), ('hz', '杭州')], default='gz', max_length=16)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]