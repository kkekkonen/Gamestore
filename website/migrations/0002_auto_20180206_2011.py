# Generated by Django 2.0 on 2018-02-06 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='price',
            field=models.FloatField(),
        ),
    ]
