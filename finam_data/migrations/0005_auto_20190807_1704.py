# Generated by Django 2.2 on 2019-08-07 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finam_data', '0004_auto_20190806_1802'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='candle',
            unique_together={('granularity', 'time', 'instrument')},
        ),
    ]