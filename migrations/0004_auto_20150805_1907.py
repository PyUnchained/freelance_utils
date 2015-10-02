# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelance_utils', '0003_auto_20150805_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='services',
            field=models.ManyToManyField(to='freelance_utils.Service'),
        ),
    ]
