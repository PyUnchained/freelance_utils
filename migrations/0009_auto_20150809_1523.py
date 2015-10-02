# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelance_utils', '0008_auto_20150807_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callbacknotification',
            name='checkout',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
