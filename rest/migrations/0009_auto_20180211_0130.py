# Generated by Django 2.0 on 2018-02-10 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0008_auto_20180204_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='token',
            field=models.CharField(default='OM5EcdGIHDwXP0a9lY6Wk3NSh47pihDy', editable=False, max_length=32),
        ),
    ]
