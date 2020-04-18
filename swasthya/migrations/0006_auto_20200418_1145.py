# Generated by Django 3.0.2 on 2020-04-18 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swasthya', '0005_medicalrecords'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='time',
        ),
        migrations.AddField(
            model_name='appointment',
            name='slot1',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='appointment',
            name='slot2',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='appointment',
            name='slot3',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='appointment',
            name='slot4',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='appointment',
            name='slot5',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='appointment',
            name='slot6',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='appointment',
            name='slot7',
            field=models.CharField(default='', max_length=100),
        ),
    ]