# Generated by Django 2.2 on 2019-07-06 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oanda', '0018_auto_20190706_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='strategy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trades', to='strategy.OandaStrategy'),
        ),
    ]
