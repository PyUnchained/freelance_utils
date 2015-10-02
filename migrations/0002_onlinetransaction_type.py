# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelance_utils', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='onlinetransaction',
            name='type',
            field=models.CharField(default='p', max_length=2, choices=[(b'AT', b'Academics Tuition'), (b'PT', b'Professional Tuition'), (b'ET', b'ECD Tuition'), (b'AE', b'Academics Exam/Practical'), (b'PE', b'Professionals Exam/Practical')]),
            preserve_default=False,
        ),
    ]
