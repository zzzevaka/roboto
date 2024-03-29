# Generated by Django 2.2 on 2019-07-06 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roboto', '0008_instrumentvalue'),
        ('strategy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='oandastrategy',
            name='instrument',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='roboto.Instrument'),
        ),
        migrations.AddField(
            model_name='oandastrategy',
            name='name',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
