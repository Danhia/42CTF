# Generated by Django 2.2.5 on 2019-09-28 16:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofileinfo',
            options={'ordering': ['-score', 'last_submission_date', 'user__username'], 'verbose_name': 'profile', 'verbose_name_plural': 'profiles'},
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='last_submission_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 28, 16, 20, 48, 164386, tzinfo=utc), verbose_name='Last Submission Date'),
        ),
    ]
