# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-19 15:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0005_auto_20171019_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofil',
            name='picture',
            field=models.ImageField(default='pictures/nopicture.png', upload_to='pictures/'),
        ),
    ]
