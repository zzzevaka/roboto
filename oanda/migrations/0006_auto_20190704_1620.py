# Generated by Django 2.2 on 2019-07-04 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oanda', '0005_trade_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='external_id',
            field=models.SmallIntegerField(blank=True),
        ),
    ]
