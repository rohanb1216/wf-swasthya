# Generated by Django 3.0.2 on 2020-04-18 15:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swasthya', '0006_auto_20200418_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]