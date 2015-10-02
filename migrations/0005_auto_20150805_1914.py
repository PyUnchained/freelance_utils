# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelance_utils', '0004_auto_20150805_1907'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='services',
        ),
        migrations.AddField(
            model_name='account',
            name='elearning_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='account',
            name='payments_active',
            field=models.BooleanField(default=True),
        ),
        migrations.DeleteModel(
            name='Service',
        ),
    ]
