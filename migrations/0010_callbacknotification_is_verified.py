# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelance_utils', '0009_auto_20150809_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='callbacknotification',
            name='is_verified',
            field=models.BooleanField(default=True),
        ),
    ]
