# Generated by Django 2.0 on 2018-02-17 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0012_auto_20180213_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='token',
            field=models.CharField(default='GAxpvpGThrpYO5azDpSc6AtWd58qDxwD', editable=False, max_length=32),
        ),
    ]