# Generated by Django 3.2 on 2021-06-14 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('runtest', '0008_auto_20210527_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testrun',
            name='portfolio_start',
            field=models.IntegerField(help_text='Backtest will start with this starting capital amount', verbose_name='Starting Capital'),
        ),
    ]