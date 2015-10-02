# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelance_utils', '0012_auto_20150813_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='p4apayment',
            name='call_back',
            field=models.ForeignKey(blank=True, to='freelance_utils.CallBackNotification', null=True),
        ),
    ]
