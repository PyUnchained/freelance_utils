# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelance_utils', '0010_callbacknotification_is_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransferPendingNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('merchant', models.CharField(max_length=50)),
                ('order', models.CharField(max_length=100, null=True)),
                ('digest', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='callbacknotification',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
