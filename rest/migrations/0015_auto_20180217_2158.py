# Generated by Django 2.0 on 2018-02-17 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0014_auto_20180217_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='token',
            field=models.CharField(default='HhhvEUhOKC0So140kNBR7EAxpPef0UyS', editable=False, max_length=32),
        ),
    ]