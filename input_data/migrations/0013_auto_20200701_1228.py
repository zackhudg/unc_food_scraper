# Generated by Django 3.0.6 on 2020-07-01 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('input_data', '0012_auto_20200625_1052'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meal',
            options={'ordering': ['date', 'meal']},
        ),
    ]