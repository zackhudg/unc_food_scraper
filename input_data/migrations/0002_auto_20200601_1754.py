# Generated by Django 3.0.6 on 2020-06-01 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('input_data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='input_data',
            name='dates',
            field=models.DateField(verbose_name='date_widget'),
        ),
    ]