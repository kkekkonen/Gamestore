# Generated by Django 2.0 on 2018-02-18 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_merge_20180218_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='category',
            field=models.CharField(choices=[('Action', 'Action'), ('Arcade', 'Arcade'), ('Indie', 'Indie'), ('Puzzle', 'Puzzle'), ('Strategy', 'Strategy')], default='a', max_length=100),
        ),
    ]