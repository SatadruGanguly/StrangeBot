# Generated by Django 3.2.4 on 2021-06-22 11:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedBotApp', '0004_auto_20210622_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='dob',
            field=models.DateField(default=datetime.date(2021, 6, 22)),
        ),
    ]
