# Generated by Django 2.0.4 on 2018-04-20 21:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('julopedia', '0002_auto_20180420_1543'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name': 'author', 'verbose_name_plural': 'authors'},
        ),
        migrations.AlterModelOptions(
            name='node',
            options={'verbose_name': 'node', 'verbose_name_plural': 'nodes'},
        ),
        migrations.RemoveField(
            model_name='node',
            name='modification_date',
        ),
        migrations.AddField(
            model_name='node',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 20, 21, 22, 52, 152178, tzinfo=utc), editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='node',
            name='modified_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 20, 21, 23, 1, 327950, tzinfo=utc)),
            preserve_default=False,
        ),
    ]