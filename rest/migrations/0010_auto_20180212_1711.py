# Generated by Django 2.0 on 2018-02-12 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0009_merge_20180212_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='token',
            field=models.CharField(default='gZD53ziYJIgco7IhA0z9tCzcZlZQra0J', editable=False, max_length=32),
        ),
    ]
