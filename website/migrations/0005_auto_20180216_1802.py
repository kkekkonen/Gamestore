# Generated by Django 2.0 on 2018-02-16 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20180211_1526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='name',
        ),
        migrations.AddField(
            model_name='category',
            name='gamecategory',
            field=models.CharField(choices=[('Act', 'Action'), ('Arc', 'Arcade'), ('Ind', 'Indie'), ('Puz', 'Puzzle'), ('Str', 'Strategy')], default='Act', max_length=3),
        ),
        migrations.AddField(
            model_name='game',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.Category'),
        ),
    ]