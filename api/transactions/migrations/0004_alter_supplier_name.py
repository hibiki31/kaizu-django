# Generated by Django 3.2.6 on 2021-09-01 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_auto_20210901_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='name',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]
