# Generated by Django 2.0 on 2018-02-11 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='category',
            field=models.CharField(choices=[('action', 'Action'), ('shooting', 'Shooting'), ('arcade', 'Arcade'), ('adventure', 'Adventure'), ('strategy', 'Strategy'), ('simulation', 'Simulation'), ('demos', 'Demos'), ('indie', 'Indie'), ('puzzle', 'Puzzle'), ('retro', 'Retro')], default='indie', max_length=20),
        ),
    ]
