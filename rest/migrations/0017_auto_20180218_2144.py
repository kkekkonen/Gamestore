# Generated by Django 2.0 on 2018-02-18 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0016_merge_20180218_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='token',
            field=models.CharField(default='n7PJN4fw5S1fXIS79ASgL5SMfgsZtK64', editable=False, max_length=32),
        ),
    ]