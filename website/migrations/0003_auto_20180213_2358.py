# Generated by Django 2.0 on 2018-02-13 21:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20180206_2011'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rightssupport',
            options={'managed': False, 'permissions': (('developer_rights', 'developers can add games'),)},
        ),
    ]
