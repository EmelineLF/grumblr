# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 03:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0015_auto_20171025_0135'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='content',
            new_name='text',
        ),
    ]
