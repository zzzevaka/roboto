# Generated by Django 2.2 on 2019-07-04 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oanda', '0008_auto_20190704_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='type',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
