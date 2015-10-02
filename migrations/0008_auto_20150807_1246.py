# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelance_utils', '0007_auto_20150807_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callbacknotification',
            name='amount',
            field=models.DecimalField(null=True, max_digits=7, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='callbacknotification',
            name='checkout',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='callbacknotification',
            name='digest',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='callbacknotification',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='callbacknotification',
            name='order',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='callbacknotification',
            name='timestamp',
            field=models.DateTimeField(null=True),
        ),
    ]
