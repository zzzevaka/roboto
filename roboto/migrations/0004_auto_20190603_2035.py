# Generated by Django 2.2 on 2019-06-03 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roboto', '0003_auto_20190603_2035'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='candle',
            unique_together={('instrument', 'time')},
        ),
    ]
