# Generated by Django 3.2.4 on 2021-06-20 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MedBotApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatrecords',
            old_name='uname',
            new_name='user_ref',
        ),
    ]
