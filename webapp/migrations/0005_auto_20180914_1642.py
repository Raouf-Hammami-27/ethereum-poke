# Generated by Django 2.1.1 on 2018-09-14 16:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20180914_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='gasUsedByTxn',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timeStamp',
            field=models.DateField(blank=True, default=datetime.datetime(2018, 9, 14, 16, 42, 46, 58187)),
        ),
    ]