# Generated by Django 2.2.6 on 2020-06-04 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vmManage', '0003_auto_20200604_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='ip',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='members',
            name='ip',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='members',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='pool',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
