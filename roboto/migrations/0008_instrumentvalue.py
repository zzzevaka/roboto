# Generated by Django 2.2 on 2019-06-14 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roboto', '0007_candle_granularity'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstrumentValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now=True)),
                ('value', models.TextField()),
                ('instrument', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_values', to='roboto.Instrument')),
            ],
            options={
                'unique_together': {('instrument', 'time')},
            },
        ),
    ]
