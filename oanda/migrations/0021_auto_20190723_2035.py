# Generated by Django 2.2 on 2019-07-23 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oanda', '0020_remove_trade_strategy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.SmallIntegerField(choices=[(0, 'create'), (1, 'fill'), (2, 'cancel')]),
        ),
    ]
