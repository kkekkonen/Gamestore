# Generated by Django 2.0 on 2018-02-11 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0011_auto_20180211_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='token',
            field=models.CharField(default='DjmyYHH4YY8h7aunsolrEGB3RHCtjkBF', editable=False, max_length=32),
        ),
    ]
