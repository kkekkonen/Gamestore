# Generated by Django 2.0 on 2018-02-03 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0004_auto_20180203_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='token',
            field=models.CharField(default='oPS8k55EkvtwJnabaPybVhQwbiCPVm7j', editable=False, max_length=32),
        ),
    ]