# Generated by Django 3.0.6 on 2020-07-01 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('input_data', '0013_auto_20200701_1228'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meal',
            options={'ordering': ['meal']},
        ),
    ]
