# Generated by Django 2.2 on 2019-07-04 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oanda', '0010_auto_20190704_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='external_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
