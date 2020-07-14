# Generated by Django 3.0.6 on 2020-06-17 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('input_data', '0009_auto_20200604_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='meal',
            field=models.TextField(choices=[('breakfast', 'breakfast'), ('brunch', 'brunch'), ('lunch', 'lunch'), ('dinner', 'dinner'), ('none', 'none')]),
        ),
        migrations.AlterField(
            model_name='option',
            name='score',
            field=models.BooleanField(null=True),
        ),
    ]