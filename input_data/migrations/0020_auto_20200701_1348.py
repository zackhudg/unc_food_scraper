# Generated by Django 3.0.6 on 2020-07-01 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('input_data', '0019_auto_20200701_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='meal',
            field=models.IntegerField(choices=[('breakfast', 0), ('brunch', 1), ('lunch', 2), ('dinner', 3), ('none', -1)]),
        ),
    ]
