# Generated by Django 3.0.6 on 2020-05-22 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_auto_20200427_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='religion',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
