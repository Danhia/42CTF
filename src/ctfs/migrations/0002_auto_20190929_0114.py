# Generated by Django 2.2.5 on 2019-09-29 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctfs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ctf',
            name='flag',
            field=models.TextField(),
        ),
    ]
