# Generated by Django 2.0 on 2018-02-19 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0017_auto_20180218_2144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apikey',
            name='user',
        ),
        migrations.DeleteModel(
            name='ApiKey',
        ),
    ]
